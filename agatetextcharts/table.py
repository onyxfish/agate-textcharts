#!/usr/bin/env python

import sys

from agatetextcharts.charts import Bars

#: Default chart width in characters
DEFAULT_WIDTH = 120

class TableCharts(object):
    def bar_chart(self, label_column_name, value_column_names, output=sys.stdout, width=DEFAULT_WIDTH):
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
        bar_chart = Bars(self, label_column_name, value_column_names, output, width)

        bar_chart.plot()
