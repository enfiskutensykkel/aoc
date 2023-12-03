#!/usr/bin/env python3
import re

s = 0
for line in open("input.txt").readlines():
    d = re.findall(r'\d', line)
    first, last = d[0], d[-1]
    s += int(first + last)
print(s)
