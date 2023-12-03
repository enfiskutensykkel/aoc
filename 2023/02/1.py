#!/usr/bin/env python3
import re

#test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
#Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
#Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
#Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
#Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


config = {"blue": 14,
          "red": 12,
          "green": 13}

expr = re.compile(r"(\d+) (green|red|blue)")

possible = 0

for line in open("input.txt").readlines():
    game = int(re.search("^Game (\d+):", line).group(1))
    parts = re.split(r"[:;]", line)
    impossible = False
    for part in parts[1:]:
        s = expr.findall(part)
        for n, c in s:
            if int(n) > config[c]:
                impossible = True
                break

        if impossible:
            break

    else:
        possible += game

print(possible)
