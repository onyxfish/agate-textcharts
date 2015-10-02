#!/usr/bin/env python

import agate
import agatetextcharts

agatetextcharts.patch()

rows = (
    ('a', '4.2'),
    ('b', '-2.7'),
    ('c', '5'),
    ('d', '0'),
    ('e', '-10'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

print 'Mixed signs'
mixed_signs = agate.Table(rows, columns)
mixed_signs.bar_chart('what', 'how_much', width=None)

rows = (
    ('a', '-4.2'),
    ('b', '-2.7'),
    ('c', '-5'),
    ('d', '0'),
    ('e', '-10'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

print ''
print 'All negative'
all_negative = agate.Table(rows, columns)
all_negative.bar_chart('what', 'how_much', width=28)

rows = (
    ('a', '4.2'),
    ('b', '2.7'),
    ('c', '0'),
    ('d', '0'),
    ('e', '10'),
)

columns = (
    ('what', agate.Text()),
    ('how_much', agate.Number()),

)

print ''
print 'All positive'
all_positive = agate.Table(rows, columns)
all_positive.bar_chart('what', 'how_much', width=28)
