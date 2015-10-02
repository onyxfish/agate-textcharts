#!/usr/bin/env python

import csv
import cStringIO as StringIO

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import agate
import agatetextcharts

class TestBarsChart(unittest.TestCase):
    def setUp(self):
        self.rows = (
            ('first', '17'),
            ('second', '2'),
            ('third', '3'),
            ('fourth', '4'),
            ('fifth', '40'),
        )

        self.columns = (
            ('what', agate.Text()),
            ('how_much', agate.Number()),
        )

        self.table = agate.Table(self.rows, self.columns)

    def test_single(self):
        output = StringIO.StringIO()

        self.table.bar_chart('what', 'how_much', output=output)

        result = output.getvalue().split('\n')

        self.assertEqual(len(result), 9)
