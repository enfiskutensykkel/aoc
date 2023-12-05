#!/usr/bin/env python3
import re
import sys

input_data = sys.stdin.read()

groups = input_data.strip().split("\n\n")

seed_pairs = [(int(x), int(y)) for x, y in re.findall(r"(\d+)\s(\d+)", groups[0])]

for group in groups[1:]:
    lines = group.split("\n")
    src, dst = re.search("^([^\-]+)-to-([^\s]+) map:$", lines[0]).groups()

    mapped = []
    for seed_start, seed_length in seed_pairs:
        # TODO split range

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
