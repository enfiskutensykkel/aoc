#!/usr/bin/env python

import re

width = 1000
claimexpr = re.compile(r'^#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)$')
fabric = [0 for i in xrange(width**2)]

claims = {}

for line in open('input').readlines():
    m = claimexpr.match(line)

    x, y = int(m.group('x')), int(m.group('y'))
    w, h = int(m.group('w')), int(m.group('h'))

    claims[m.group('id')] = (x, y, w, h)

    for j in range(y, y+h):
        for i in range(x, x+w):
            fabric[j * width + i] += 1

print len(filter(lambda x: x >= 2, fabric))

for claim in claims:
    x, y, w, h = claims[claim]

    continuous = True
    for j in range(y, y+h):
        for i in range(x, x+w):
            if fabric[j * width + i] != 1:
                continuous = False
                break

        if not continuous:
            break

    if continuous:
        print claim
