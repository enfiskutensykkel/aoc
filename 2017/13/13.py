#!/usr/bin/env python

class Layer(object):
    def __init__(self, d, r):
        self.depth = d
        self.range = r
        self.scanner = 0
        self.direction = 1

    def move_scanner(self):
        if self.scanner == 0 or self.scanner == self.depth:
            self.direction *= -1

        self.scanner += self.direction


data = """0: 3
1: 2
4: 4
6: 4""".split("\n")

layers = []
depths = {}
