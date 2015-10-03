#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    from cDecimal import Decimal
except ImportError:
    from decimal import Decimal

import agate
from agatetextcharts.charts.base import Chart
from agatetextcharts.utils import round_limit

#: Default character to render for bar units
DEFAULT_BAR_CHAR = u'░'

DEFAULT_HORIZONTAL_SEP = u'-'
DEFAULT_VERTICAL_SEP = u'|'
DEFAULT_ZERO_SEP = u'▓'
DEFAULT_TICK_MARKER = u'+'

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
        available_width -= 2    # left and right border

        self.plot_width = available_width

        # Calculate dimensions
        min_value = self.value_column.aggregate(agate.Min())
        self.x_min = round_limit(min_value)
        max_value = self.value_column.aggregate(agate.Max())
        self.x_max = round_limit(max_value)

        self.zero_line = None
        self.plot_positive_width = 0
        self.plot_negative_width = 0

        # All positive values
        if self.x_min >= 0:
            self.plot_positive_width = self.plot_width
        # All negative values
        elif self.x_max <= 0:
            self.plot_negative_width = self.plot_width
        # Mixed positive and negative values
        else:
            spread = self.x_max - self.x_min
            positive_portion = (self.x_max / spread)

            # subtract one for zero line
            self.zero_line = (self.plot_width - 1) - int(self.plot_width * positive_portion)
            self.plot_positive_width = (self.plot_width - 1) - self.zero_line
            self.plot_negative_width = (self.plot_width - 1) - self.plot_positive_width

    def project(self, value):
        if value >= 0:
            return self.plot_negative_width + int((self.plot_positive_width * (value / self.x_max)).to_integral_value())
        else:
            return int((self.plot_negative_width * (value / self.x_min)).to_integral_value())

    def calculate_ticks(self):
        # Calculate ticks
        self.ticks = {}

        # First tick
        self.ticks[-1] = unicode(self.x_min)

        # Zero tick
        if self.zero_line:
            self.ticks[self.zero_line] = u'0'

        # Last tick
        self.ticks[self.plot_width] = unicode(self.x_max)

        if self.x_min >= 0:
            # Halfway between min and max
            value = self.x_max * Decimal('0.5')
            self.ticks[self.project(value)] = unicode(value)
        elif self.x_max <= 0:
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
        top_line += ' ' * (self.plot_width + 3)
        self.write(top_line)

        # Bars
        for i, label in enumerate(self.label_column):
            value = self.value_column[i]

            if value == 0:
                bar_width = 0
            elif value > 0:
                bar_width = int((self.plot_positive_width * (value / self.x_max)).to_integral_value())
            elif value < 0:
                bar_width = int((self.plot_negative_width * (value / self.x_min)).to_integral_value())

            label_text = label.rjust(self.max_label_width)
            bar = DEFAULT_BAR_CHAR * bar_width
            value_text = unicode(value)

            if value >= 0:
                gap = (u' ' * self.plot_negative_width)

                if self.zero_line:
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

                if self.zero_line:
                    bar += DEFAULT_ZERO_SEP

            bar_text = (gap + bar).ljust(self.plot_width)

            line = '%s ' % label_text

            if self.x_min == 0:
                line += DEFAULT_ZERO_SEP
            else:
                line += ' '

            line += bar_text

            if self.x_max == 0:
                line += DEFAULT_ZERO_SEP
            else:
                line += ' '

            self.write(line)

        # Chart bottom
        plot_edge = DEFAULT_TICK_MARKER

        for i in xrange(self.plot_width):
            if i in self.ticks:
                plot_edge += DEFAULT_TICK_MARKER
            else:
                plot_edge += DEFAULT_HORIZONTAL_SEP

        plot_edge += DEFAULT_TICK_MARKER

        plot_edge = plot_edge.rjust(self.width)
        self.write(plot_edge)

        # Ticks
        tick_text = u' ' * self.width

        for tick, label in self.ticks.items():
            pos = (self.width - self.plot_width - 1) + tick - (len(label) / 2)
            tick_text = tick_text[:pos] + label + tick_text[pos + len(label):]

        self.write(tick_text)

        # X-axis label
        x_label = self.x_label.center(self.plot_width + 2).rjust(self.width)
        self.write(x_label)
