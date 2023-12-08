#!/usr/bin/env python3
from sys import stdin
import re

expr = re.compile(r"^([^\s]+) = \(([^,]+), ([^\)]+)\)$")

instructions, graph_lines = stdin.read().strip().split("\n\n")

graph = {}

nodes = []
for line in graph_lines.split("\n"):
    node, left, right = expr.match(line).groups()
    graph[node] = (left, right)
    if node[-1] == "A":
        nodes.append(node)

def factorization(k):
	if k == 1:
		return [1]

	step = 2
	lim = k // 2
	while step <= lim:
		if k % step == 0:
			return factorization(k // step) + [step]

		step += 1

	return [k]

def num_steps(node, graph, instructions):
    steps = 0

    while node[-1] != "Z":
        instr = instructions[steps % len(instructions)]
        node = graph[node][0 if instr == "L" else 1]
        steps += 1

    target = node

    instr = instructions[steps % len(instructions)]
    node = graph[node][0 if instr == "L" else 1]
    cycle = 1

    while node[-1] != "Z":
        instr = instructions[cycle % len(instructions)]
        node = graph[node][0 if instr == "L" else 1]
        cycle += 1

    if node != target:
        print("multiple cycles")

    return steps, cycle


steps = [num_steps(node, graph, instructions)[1] for node in nodes]

m = max(steps)
for s in steps:
    print(factorization(s))


#
#min_common = 10000000000
#
#for f in factors[0]:
#    for facs in factors[1:]:
#        for g in facs:
#            if f == g and f < min_common:
#                min_common = f
#
#for step in steps:
#    print(step)
