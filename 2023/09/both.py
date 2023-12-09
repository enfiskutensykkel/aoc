#!/usr/bin/env python3
from sys import stdin

lines = stdin.read().strip().split("\n")


def extrapolate_fwd(seq):
    if not all(x == 0 for x in seq):
        diffs = []
        for i in range(1, len(seq)):
            diffs.append(seq[i] - seq[i-1])

        extrapolate_fwd(diffs)

        seq.append(seq[-1] + diffs[-1])

    else:
        seq.append(0)

total = 0

for line in lines:
    nums = [int(x) for x in line.split()]
    extrapolate_fwd(nums)
    total += nums[-1]

print(total)


def extrapolate_bkwd(seq):
    if not all(x == 0 for x in seq):
        diffs = []
        for i in range(1, len(seq)):
            diffs.append(seq[i] - seq[i-1])

        extrapolate_bkwd(diffs)

        seq.insert(0, seq[0] - diffs[0])

    else:
        seq.insert(0, 0)

total = 0
for line in lines:
    nums = [int(x) for x in line.split()]
    extrapolate_bkwd(nums)
    total += nums[0]

print(total)
