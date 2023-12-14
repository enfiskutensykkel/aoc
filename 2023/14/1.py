#!/usr/bin/env python3
from sys import stdin

rows = []
loads = []

for row in stdin.read().strip().splitlines():

    loads.insert(0, 0)
    rows.insert(0, set())

    for x, c in enumerate(row):
        if c == '#':
            rows[0].add(x)

        elif c == 'O':
            to_row = 0
            while to_row+1 < len(rows) and x not in rows[to_row+1]:
                to_row += 1

            rows[to_row].add(x)
            loads[to_row] += 1

print(sum(l * (i+1) for i, l in enumerate(loads)))
