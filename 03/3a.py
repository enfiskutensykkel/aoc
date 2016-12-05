#!/usr/bin/env python

possible = 0

for line in open('input').readlines():
    abc = [int(x) for x in line.split()]
    abc.sort()

    if abc[0] + abc[1] > abc[2]:
        possible += 1

print possible
