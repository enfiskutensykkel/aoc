#!/usr/bin/env python
import re

pattern = re.compile(r'Disc #(?P<slot>\d+) has (?P<n>\d+) positions; at time=(?P<t>\d+), it is at position (?P<curr>\d+).')

discs = []

#for line in open('test').readlines():
for line in open('input').readlines():
    slot = int(pattern.match(line).group('slot'))
    npos = int(pattern.match(line).group('n'))
    time = int(pattern.match(line).group('t'))
    curr = int(pattern.match(line).group('curr'))

    discs.append((slot, (curr + slot + 1) % npos, npos))

discs.append((slot+1, (0 + (slot+1) + 1) % 11, 11))


t = 0
aligned = False
while not aligned:

    ndiscs = []
    aligned = True
    for disc in discs:
        slot, curr, npos = disc
        curr = (curr + t) % npos
        if curr != 0:
            aligned = False
        ndiscs.append((slot, curr, npos))

    t += 1

print t
