#!/usr/bin/env python3
from sys import stdin


def test_arrangement(group, counts):
    i = 0
    j = -1
    streaks = []
    while i < len(group):
        if group[i] == '.':
            if j != i - 1:
                streaks.append(i - j - 1)
            j = i
        i += 1

    if j != i - 1:
        streaks.append(i - j - 1)

    return streaks == counts


def permutate(group, counts, start, dmg, op):
    if start >= len(group) or (dmg == 0 and op == 0):
        return 1 if test_arrangement(group, counts) else 0

    p = 0
    if group[start] == '?':
        if dmg > 0:
            group[start] = '#'
            p += permutate(group, counts, start+1, dmg-1, op)

        if op > 0:
            group[start] = '.'
            p += permutate(group, counts, start+1, dmg, op-1)

        group[start] = '?'

    else:
        p = permutate(group, counts, start + 1, dmg, op)
    return p


s = 0
for row in stdin.read().strip().split("\n"):
    group, counts = row.split()
    counts = [int(x) for x in counts.split(",")]
    l = permutate(list(group), counts, 0, sum(counts), len(group) - sum(counts))
    s += l

print(s)
