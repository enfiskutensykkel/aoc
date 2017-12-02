#!/usr/bin/env python

keypad = \
"""xxxxxxx
xxx1xxx
xx234xx
x56789x
xxABCxx
xxxDxxx
xxxxxxx"""

row = 3
col = 1

w = 8

for line in open("input.txt").readlines():
#for line in ['ULL', 'RRDDD', 'LURDL', 'UUUUD']:
    for c in line:
        if c == 'U' and keypad[(row - 1) * w + col] != 'x':
            row -= 1
        elif c == 'D' and keypad[(row + 1) * w + col] != 'x':
            row += 1
        elif c == 'L' and keypad[row * w + (col - 1)] != 'x':
            col -= 1
        elif c == 'R' and keypad[row * w + (col + 1)] != 'x':
            col += 1
    print keypad[row * w + col],

print
