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
    def test_all_positive(self):
        rows = (
            ('a', '4.2'),
            ('b', '2.7'),
            ('c', '10'),
            ('d', '0'),
            ('e', '10'),
        )

        columns = (
            ('what', agate.Text()),
            ('how_much', agate.Number()),

        )

        table = agate.Table(rows, columns)
        table.bar_chart('what', 'how_much', size=(18, 100))

        output = StringIO.StringIO()

        table.bar_chart('what', 'how_much', output=output)

        with open('tests/compare/test_all_positive.txt') as f:
            compare = f.read()

        self.assertEqual(compare, output.getstring())
