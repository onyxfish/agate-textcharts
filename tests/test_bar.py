#!/usr/bin/env python

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

        output = StringIO.StringIO()

        table.bar_chart('what', 'how_much', output=output, width=18)

        with open('tests/compare/test_all_positive.txt') as f:
            compare = f.read()

        self.assertEqual(compare, output.getvalue())

    def test_all_negative(self):
        rows = (
            ('a', '-4.2'),
            ('b', '-2.7'),
            ('c', '-10'),
            ('d', '0'),
            ('e', '-10'),
        )

        columns = (
            ('what', agate.Text()),
            ('how_much', agate.Number()),

        )

        table = agate.Table(rows, columns)

        output = StringIO.StringIO()

        table.bar_chart('what', 'how_much', output=output, width=18)

        with open('tests/compare/test_all_negative.txt') as f:
            compare = f.read()

        self.assertEqual(compare, output.getvalue())

    def test_mixed_signs(self):
        rows = (
            ('a', '4.2'),
            ('b', '-2.7'),
            ('c', '10'),
            ('d', '0'),
            ('e', '-10'),
        )

        columns = (
            ('what', agate.Text()),
            ('how_much', agate.Number()),

        )

        table = agate.Table(rows, columns)

        output = StringIO.StringIO()

        table.bar_chart('what', 'how_much', output=output, width=29)

        with open('tests/compare/test_mixed_signs.txt') as f:
            compare = f.read()

        self.assertEqual(compare, output.getvalue())
