#!/usr/bin/env python3
import re


expr = re.compile(r"(\d+) (green|red|blue)")

s = 0
for line in open("input.txt").readlines():
    game = int(re.search("^Game (\d+):", line).group(1))
    parts = re.split(r"[:;]", line)
    cubes = {"green": 0,
             "blue": 0,
             "red": 0}
    for part in parts[1:]:
        ss = expr.findall(part)
        for n, c in ss:
            if int(n) > cubes[c]:
                cubes[c] = int(n)

    p = 1
    for n in cubes.values():
        p *= n
    s += p
print(s)
