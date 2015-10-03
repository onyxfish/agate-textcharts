#!/usr/bin/env python

class Chart(object):
    """
    Base class for all chart renderers.
    """
    def write(self, line):
        self.output.write(line + '\n')

    def plot(self):
        raise NotImplementedError
