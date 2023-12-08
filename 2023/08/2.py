#!/usr/bin/env python3
from sys import stdin
import re

def gcd(a, b):
    while a > 0:
        a, b = b % a, a
    return b

def lcms(*args):
    r = args[0]
    for i in range(1, len(args)):
        r = r * args[i] // gcd(r, args[i])
    return r

expr = re.compile(r"^([^\s]+) = \(([^,]+), ([^\)]+)\)$")
instructions, graph_lines = stdin.read().strip().split("\n\n")

graph = {}
nodes = []
for line in graph_lines.split("\n"):
    node, left, right = expr.match(line).groups()
    graph[node] = (left, right)
    if node[-1] == "A":
        nodes.append(node)

def num_steps(node, graph, instructions):
    steps = 0
    visited = set()

    while True:
        idx = steps % len(instructions)
        if node[-1] == "Z": #and (node, idx) in visited:
            return steps

        visited.add((node, idx))
        instr = instructions[idx]
        node = graph[node][0 if instr == "L" else 1]
        steps += 1

steps = [num_steps(node, graph, instructions) for node in nodes]
print(lcms(*steps))
