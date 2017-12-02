#!/usr/bin/env python

checksum = 0

for row in open("input").readlines():
    values = [int(x) for x in row.split()]
    checksum += max(values) - min(values)

print checksum
