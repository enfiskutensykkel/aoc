#!/usr/bin/env python3
from sys import stdin

def seek(group):
    i = 0
    j = -1
    streaks = []
    while i < len(group):
        if group[i] != '#':
            if j != i - 1:
                streaks.append(i - j - 1)
            j = i
        i += 1

    if j != i - 1:
        streaks.append(i - j - 1)

    return streaks

def permutations(group, counts, start):
    if start >= len(group):
        return 1 if seek(group) == counts else 0

    p = 0
    if group[start] == '?':
        group[start] = '#'
        p += permutations(group, counts, start + 1)
        group[start] = '.'
        p += permutations(group, counts, start + 1)
        group[start] = '?'
    else:
        p = permutations(group, counts, start + 1)
    return p


s = 0
for row in stdin.read().strip().split('\n'):
    group, counts = row.split()
    l = permutations(list(group), [int(x) for x in counts.split(',')], 0)
    s += l

print(s)
