#!/usr/bin/env python3
from sys import stdin


def test_arrangement(group, start, count):
    i = start
    length = start + count

    while i < length:
        if i >= len(group):
            return False

        if group[i] == ".":
            return False

        i += 1

    if i < len(group) and group[i] == "#":
        return False

    return True


def permutations(group, counts, start, idx, matches):
    if idx >= len(counts):
        while start < len(group):
            if group[start] == "#":
                return 0
            start += 1
        return 1

    key = (group[start:], counts[idx:])
    r = matches.get(key, -1)
    if r >= 0:
        return r

    while start < len(group) and group[start] == ".":
        start += 1

    if start >= len(group):
        return 1 if idx >= len(counts) else 0

    count = counts[idx]

    p = 0
    if test_arrangement(group, start, count):
        p += permutations(group, counts, start+count+1, idx + 1, matches)

    if group[start] != "#":
        p += permutations(group, counts, start+1, idx, matches)

    matches[key] = p
    return p


matches = {}
total_part1 = 0
total_part2 = 0
for row in stdin.read().strip().split("\n"):
    group, counts = row.split()

    long_group = "?".join([group] * 5)
    long_counts = tuple(int(x) for x in ",".join([counts] * 5).split(","))

    counts = tuple(int(x) for x in counts.split(","))

    total_part1 += permutations(group, counts, 0, 0, matches)
    total_part2 += permutations(long_group, long_counts, 0, 0, matches)

print(total_part1)
print(total_part2)
