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

def gcd(a, b):
    while a > 0:
        a, b = b % a, a
    return b

def lcm(a, b):
    return (a*b) // gcd(a, b)

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

p = 1
for s in steps:
    p *= s

