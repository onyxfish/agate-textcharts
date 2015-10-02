#!/usr/bin/env python

import agate
import agatetextcharts

agatetextcharts.patch()

rows = (
    ('a', '4'),
    ('b', '2'),
    ('c', '4'),
    ('d', '0'),
    ('e', '4'),
    ('f', '4'),
    ('g', '17'),
    ('h', '-4'),
    ('idifjalsdjkf', '4'),
    ('j', '3'),
    ('k', '3'),
    ('l', '3'),
    ('n', '4'),
    ('o', '4'),
    ('p', '-2'),
    ('q', '-4'),
    ('r', '4'),
    ('s', '4'),
    ('t', '1'),
    ('u', '4'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

table = agate.Table(rows, columns)

table.bar_chart('what', 'how_much')
