#!/usr/bin/env python

import re

#instructions = """Step C must be finished before step A can begin.
#Step C must be finished before step F can begin.
#Step A must be finished before step B can begin.
#Step A must be finished before step D can begin.
#Step B must be finished before step E can begin.
#Step D must be finished before step E can begin.
#Step F must be finished before step E can begin."""

instructions = open('input').read()

steps = set()
deps = {}
for step, depending in re.findall(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", instructions):
    if not depending in deps:
        deps[depending] = []
    deps[depending].append(step)

    steps.add(step)
    steps.add(depending)


string = ""
while len(steps) > 0:
    for step in sorted(steps):
        if not step in deps or len(deps[step]) == 0:
            steps.remove(step)
            break

    string += step
    for dep in deps:
        if step in deps[dep]:
            deps[dep].remove(step)

print string
