#!/usr/bin/env python

keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
        ]

row = 1
col = 1

for line in open("input.txt").readlines():
#for line in ['ULL', 'RRDDD', 'LURDL', 'UUUUD']:
    for c in line:
        if c == 'U':
            row = max(row - 1, 0)
        elif c == 'D':
            row = min(row + 1, 2)
        elif c == 'L':
            col = max(col - 1, 0)
        elif c == 'R':
            col = min(col + 1, 2)
    print keypad[row][col],

print
