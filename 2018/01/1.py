#!/usr/bin/env python

freq = 0

for line in open('input').readlines():
    freq += int(line.strip())

print freq
