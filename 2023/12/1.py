#!/usr/bin/env python3
from sys import stdin


def test_arrangement(group, counts):
    i = 0
    j = -1

    streaks = 0

    while i < len(group):
        if group[i] == '.':
            if j != i - 1:
                if streaks >= len(counts) or counts[streaks] != i - j - 1:
                    return False
                streaks += 1
            j = i
        i += 1

    if j != i - 1:
        if streaks >= len(counts) or counts[streaks] != i - j - 1:
            return False
        streaks += 1

    return streaks == len(counts)


def permutate(group, counts, start, dmg, op):
    if start >= len(group) or (dmg == 0 and op == 0):
        return 1 if test_arrangement(group, counts) else 0

    if group[start] == '?':
        permutations = 0

        if dmg > 0:
            group[start] = '#'
            p = permutate(group, counts, start+1, dmg-1, op)
            permutations += p

        if op > 0:
            group[start] = '.'
            p = permutate(group, counts, start+1, dmg, op-1)
            permutations += p

        group[start] = '?'

    else:
        permutations = permutate(group, counts, start + 1, dmg, op)

    return permutations


s = 0
for row in stdin.read().strip().split("\n"):
    group, counts = row.split()
    counts = [int(x) for x in counts.split(",")]

    l = permutate(list(group), counts, 0, sum(counts), len(group) - sum(counts))
    s += l

print(s)
