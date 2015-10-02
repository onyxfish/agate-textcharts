#!/usr/bin/env python

import agate
import agatetextcharts

agatetextcharts.patch()

rows = (
    ('a', '4'),
    ('b', '-2'),
    ('c', '4'),
    ('d', '0'),
    ('e', '4'),
    ('f', '4'),
    ('g', '10'),
    ('h', '-10'),
    ('j', '3'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

table = agate.Table(rows, columns)

table.bar_chart('what', 'how_much', size=(29, 100))
