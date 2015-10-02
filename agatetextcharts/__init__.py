#!/usr/bin/env python

def patch():
    """
    Patch the features of this library onto agate's core :class:`.Table`.
    """
    import agate
    from agatetextcharts.table import TableCharts

    agate.Table.monkeypatch(TableCharts)
