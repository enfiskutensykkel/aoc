#!/usr/bin/env python

data = open("input").read().strip()

s = 0
prev = data[-1]
for c in data:
    if c == prev:
        s += int(c)
    prev = c

print s
