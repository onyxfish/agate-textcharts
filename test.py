#!/usr/bin/env python

import agate
import agatetextcharts

agatetextcharts.patch()

rows = (
    ('a', '4'),
    ('b', '-2'),
    ('c', '10'),
    ('d', '0'),
    ('e', '-10'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

mixed_signs = agate.Table(rows, columns)
mixed_signs.bar_chart('what', 'how_much', size=(29, 100))

rows = (
    ('a', '-4'),
    ('b', '-2'),
    ('c', '-10'),
    ('d', '0'),
    ('e', '-10'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

all_negative = agate.Table(rows, columns)
all_negative.bar_chart('what', 'how_much', size=(29, 100))

rows = (
    ('a', '4'),
    ('b', '2'),
    ('c', '10'),
    ('d', '0'),
    ('e', '10'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

all_positive = agate.Table(rows, columns)
all_positive.bar_chart('what', 'how_much', size=(29, 100))
