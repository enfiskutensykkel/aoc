#!/usr/bin/env python3
from sys import stdin

def extrapolate(seq):
    if not all(x == 0 for x in seq):
        diffs = [seq[i] - seq[i-1] for i in range(1, len(seq))]
        f, b = extrapolate(diffs)
        return seq[0] - f, seq[-1] + b

    else:
        return 0, 0

part1 = 0
part2 = 0

lines = stdin.read().strip().split("\n")
for line in lines:
    a, b = extrapolate([int(x) for x in line.split()])
    part2 += a
    part1 += b

print(part1)
print(part2)
