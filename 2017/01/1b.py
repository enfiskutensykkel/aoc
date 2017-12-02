#!/usr/bin/env python

data = open("input").read().strip()

s = 0
p = len(data) / 2
for i, c in enumerate(data):
    if c == data[p]:
        s += int(c)
    p = (p + 1) % len(data)

print s
