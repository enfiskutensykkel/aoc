#!/usr/bin/env python3
import re
import sys

input_data = sys.stdin.read()

groups = input_data.strip().split("\n\n")

seeds = [int(x) for x in re.findall(r"\d+", groups[0])]

for group in groups[1:]:
    lines = group.split("\n")
    mapped = []
    for seed in seeds:
        for line in lines[1:]:
            dst, src, length = (int(x) for x in re.findall("\d+", line))
            if src <= seed and seed < (src+length):
                offset = seed - src
                mapped.append(dst + offset)
                break
        else:
            mapped.append(seed)

    seeds = mapped

print(min(seeds))
