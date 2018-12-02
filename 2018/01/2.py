#!/usr/bin/env python

data = [int(line.strip()) for line in open('input').readlines()]

freq = set()
curr = 0
freq.add(0)
repeat = None

while repeat is None:
    for value in data:
        curr += value
        if curr in freq:
            repeat = curr
            break
        freq.add(curr)

print repeat
