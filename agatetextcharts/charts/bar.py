#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    from cDecimal import Decimal, ROUND_FLOOR, ROUND_CEILING
except ImportError:
    from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING

import agate
from agatetextcharts.charts.base import Chart
from agatetextcharts.utils import round_limit

#: Default character to render for bar units
DEFAULT_BAR_CHAR = u'░'

DEFAULT_HORIZONTAL_SEP = u'-'
DEFAULT_VERTICAL_SEP = u'|'
DEFAULT_ZERO_SEP = u'▓'
DEFAULT_TICK_MARKER = u'+'

ALL_POSITIVE = 0
ALL_NEGATIVE = 1
MIXED_SIGNS = 2

class Bars(Chart):
    """
    Plots a bar chart.

    See :meth:`TableCharts._plot` for an explanation of keyword arguments.

    :param label_column_name: The name of a column in the source to be used for
        the vertical axis labels. Must refer to a column containing
        :class:`.Text`, :class:`.Number` or :class:`.Date` data.
    :param value_column_names: One or more column names in the source, each of
        which will used to define the horizontal width of a bar. Must refer to a
        column containing :class:`.Number` data.
    """
    def __init__(self, table, label_column_name, value_column_names, output, width):
        self.y_label = label_column_name
        self.label_column = table.columns[label_column_name]

        if not isinstance(self.label_column.data_type, agate.Text):
            raise ValueError('Only Text data is supported for bar chart labels.')

        if isinstance(value_column_names, basestring):
            value_column_names = [value_column_names]

        # TODO: support multiple columns
        if len(value_column_names) > 1:
            raise NotImplementedError

        self.x_label = value_column_names[0]
        self.value_column = table.columns[value_column_names[0]]

        if not isinstance(self.value_column.data_type, agate.Number):
            raise ValueError('Only Number data is supported for bar chart values.')

        self.output = output
        self.width = width

        self.calculate_dimensions()
        self.calculate_ticks()

    def calculate_dimensions(self):
        available_width = self.width
        self.max_label_width = max(self.label_column.aggregate(agate.MaxLength()), len(self.y_label))
        available_width -= self.max_label_width + 1

        self.plot_width = available_width

        # Calculate dimensions
        min_value = self.value_column.aggregate(agate.Min())
        self.x_min = round_limit(min_value)
        max_value = self.value_column.aggregate(agate.Max())
        self.x_max = round_limit(max_value)

        if self.x_min >= 0:
            self.signs = ALL_POSITIVE
        elif self.x_max <= 0:
            self.signs = ALL_NEGATIVE
        else:
            self.signs = MIXED_SIGNS

        if self.signs == ALL_POSITIVE:
            self.plot_negative_width = 0
            self.zero_line = 0
            self.plot_positive_width = self.plot_width - 1
        elif self.signs == ALL_NEGATIVE:
            self.plot_negative_width = self.plot_width - 1
            self.zero_line = self.plot_width - 1
            self.plot_positive_width = 0
        else:
            spread = self.x_max - self.x_min
            negative_portion = (self.x_min.copy_abs() / spread)

            # Subtract one for zero line
            self.plot_negative_width = int(((self.plot_width - 1) * negative_portion).to_integral_value())
            self.zero_line = self.plot_negative_width
            self.plot_positive_width = self.plot_width - (self.plot_negative_width + 1)

    def project(self, value):
        if value >= 0:
            return self.plot_negative_width + int((self.plot_positive_width * (value / self.x_max)).to_integral_value())
        else:
            return self.plot_negative_width - int((self.plot_negative_width * (value / self.x_min)).to_integral_value())

    def calculate_ticks(self):
        # Calculate ticks
        self.ticks = {}

        # First tick
        self.ticks[0] = unicode(self.x_min)

        # Zero tick
        if self.signs == MIXED_SIGNS:
            self.ticks[self.zero_line] = u'0'

        # Last tick
        self.ticks[self.plot_width - 1] = unicode(self.x_max)

        if self.signs == ALL_POSITIVE:
            # Halfway between min and max
            value = self.x_max * Decimal('0.5')
            self.ticks[self.project(value)] = unicode(value)
        elif self.signs == ALL_NEGATIVE:
            # Halfway between min and max
            value = self.x_min * Decimal('0.5')
            self.ticks[self.project(value)] = unicode(value)
        else:
            # Halfway between min and 0
            value = self.x_min * Decimal('0.5')
            self.ticks[self.project(value)] = unicode(value)

            # Halfway between 0 and max
            value = self.x_max * Decimal('0.5')
            self.ticks[self.project(value)] = unicode(value)

    def plot(self):
        # Chart top
        top_line = self.y_label.rjust(self.max_label_width)
        self.write(top_line)

        # Bars
        for i, label in enumerate(self.label_column):
            value = self.value_column[i]

            if value == 0:
                bar_width = 0
            elif value > 0:
                bar_width = self.project(value) - self.plot_negative_width
            elif value < 0:
                bar_width = self.plot_negative_width - self.project(value)

            label_text = label.rjust(self.max_label_width)
            bar = DEFAULT_BAR_CHAR * bar_width
            value_text = unicode(value)

            if value >= 0:
                gap = (u' ' * self.plot_negative_width)

                if self.signs == ALL_POSITIVE:
                    gap = DEFAULT_ZERO_SEP + gap
                else:
                    gap += DEFAULT_ZERO_SEP

                if value != 0:
                    if len(bar) + len(value_text) + 1 < self.plot_positive_width:
                        bar += ' %s' % value_text
            else:
                gap = u''

                if len(bar) + len(value_text) + 1 < self.plot_negative_width:
                    gap = (u' ' * int(self.plot_negative_width - bar_width - len(value_text) - 1)) + value_text + ' '
                else:
                    gap += (u' ' * int(self.plot_negative_width - bar_width))

                if self.signs == ALL_NEGATIVE or self.signs == MIXED_SIGNS:
                    bar += DEFAULT_ZERO_SEP

            bar_text = (gap + bar).ljust(self.plot_width)

            line = '%s ' % label_text
            line += bar_text

            self.write(line)

        # Chart bottom
        plot_edge = ''

        for i in xrange(self.plot_width):
            if i in self.ticks:
                plot_edge += DEFAULT_TICK_MARKER
            else:
                plot_edge += DEFAULT_HORIZONTAL_SEP

        plot_edge = plot_edge.rjust(self.width)
        self.write(plot_edge)

        # Ticks
        tick_text = u' ' * self.width

        for tick, label in self.ticks.items():
            pos = (self.width - self.plot_width) + tick - (len(label) / 2)
            tick_text = tick_text[:pos] + label + tick_text[pos + len(label):]

        self.write(tick_text)

        # X-axis label
        x_label = self.x_label.center(self.plot_width + 1).rjust(self.width)
        self.write(x_label)
