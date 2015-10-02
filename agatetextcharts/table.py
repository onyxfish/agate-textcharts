#!/usr/bin/env python
# -*- coding: utf8 -*-

import math
import sys

import agate
# from agatecharts.charts import Bars, Columns, Lines, Scatter
from agatetextcharts.utils import round_limit

#: Default rendered chart size in characters
DEFAULT_SIZE = (120, 120)

#: Default character to render for bar units
DEFAULT_BAR_CHAR = u'X'

DEFAULT_HORIZONTAL_SEP = '-'
DEFAULT_VERTICAL_SEP = '|'

class TableCharts(object):
    def bar_chart(self, label_column_name, value_column_names, output=sys.stdout, size=DEFAULT_SIZE):
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
        if isinstance(value_column_names, basestring):
            value_column_names = [value_column_names]

        if len(value_column_names) > 1:
            raise NotImplementedError

        label_column = self.columns[label_column_name]

        if not isinstance(label_column.data_type, agate.Text):
            raise ValueError('Only Text data is supported for bar chart labels.')

        value_column =  self.columns[value_column_names[0]]

        if not isinstance(value_column.data_type, agate.Number):
            raise ValueError('Only Number data is supported for bar chart values.')

        available_width = size[0]
        max_label_width = max(label_column.aggregate(agate.MaxLength()), len(label_column_name))
        available_width -= max_label_width
        available_width -= 2    # ': '
        available_width -= 2    # left and right border

        plot_width = available_width

        # Calculate dimensions
        min_value = value_column.aggregate(agate.Min())
        x_min = round_limit(min_value)
        max_value = value_column.aggregate(agate.Max())
        x_max = round_limit(max_value)

        # All positive values
        if x_min >= 0:
            zero_line = None
            plot_positive_width = plot_width
            plot_negative_width = 0
        # All negative values
        elif x_max <= 0:
            zero_line = None
            plot_positive_width = 0
            plot_negative_width = plot_width
        # Mixed positive and negative values
        else:
            spread = x_max - x_min
            positive_portion = (x_max / spread)

            # subtract one for zero line
            zero_line = (plot_width - 1) - int(plot_width * positive_portion)
            plot_positive_width = (plot_width - 1) - zero_line
            plot_negative_width = (plot_width - 1) - plot_positive_width

        # Calculate ticks
        ticks = {}

        ticks[0] = unicode(x_min)

        if zero_line:
            ticks[zero_line] = '0'

        ticks[plot_width - 1] = unicode(x_max)

        # Chart top
        y_label = label_column_name.center(max_label_width + 2)
        y_label += '-' * (plot_width + 2)
        output.write(y_label + '\n')

        # Bars
        for i, label in enumerate(label_column):
            value = value_column[i]

            if value == 0:
                bar_width = 0
            elif value > 0:
                bar_width = int(plot_positive_width * (value / x_max))
            elif value < 0:
                bar_width = int(plot_negative_width * (value / x_min))

            label_text = label.rjust(max_label_width)

            bar = DEFAULT_BAR_CHAR * bar_width

            # value_text = unicode(value)
            #
            # if bar_width + len(value_text) + 1 < plot_width:
            #     bar += ' %s' % value_text


            if value >= 0:
                gap = (' ' * plot_negative_width)

                if zero_line:
                    gap += '|'
            else:
                gap = (' ' * int(plot_negative_width - bar_width))

                if zero_line:
                    bar += '|'

            bar_text = (gap + bar).ljust(plot_width)

            line = '%s: |%s|' % (label_text, bar_text)

            output.write(line + '\n')

        # Chart bottom
        plot_edge = '|'

        for i in xrange(plot_width):
            if i in ticks:
                plot_edge += '+'
            else:
                plot_edge += '-'

        plot_edge += '|'

        plot_edge = plot_edge.rjust(size[0])
        output.write(plot_edge + '\n')

        # Ticks
        tick_text = ' ' * size[0]

        for tick, label in ticks.items():
            pos = (size[0] - plot_width - 1) + tick - (len(label) / 2)
            tick_text = tick_text[:pos] + label + tick_text[pos + len(label):]

        output.write(tick_text + '\n')

        # X-axis label
        x_label = value_column_names[0].center(plot_width + 2).rjust(size[0])
        output.write(x_label + '\n')
