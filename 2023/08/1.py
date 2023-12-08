#!/usr/bin/env python3
from sys import stdin
import re

expr = re.compile(r"^([^\s]+) = \(([^,]+), ([^\)]+)\)$")

instructions, graph_lines = stdin.read().strip().split("\n\n")

graph = {}

for line in graph_lines.split("\n"):
    node, left, right = expr.match(line).groups()
    graph[node] = (left, right)

node = "AAA"
goal = "ZZZ"
steps = 0

while node != goal:
    instr = instructions[steps % len(instructions)]
    node = graph[node][0 if instr == "L" else 1]
    steps += 1

print(steps)
