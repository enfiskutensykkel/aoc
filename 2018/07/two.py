#!/usr/bin/env python

from collections import deque
import re

n_cost = 60
n_workers = 5
instructions = open('input').read()

#n_cost = 0
#n_workers = 2
#instructions = """Step C must be finished before step A can begin.
#Step C must be finished before step F can begin.
#Step A must be finished before step B can begin.
#Step A must be finished before step D can begin.
#Step B must be finished before step E can begin.
#Step D must be finished before step E can begin.
#Step F must be finished before step E can begin."""

steps = set()
deps = {}
for step, depending in re.findall(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", instructions):
    if not depending in deps:
        deps[depending] = []
    deps[depending].append(step)

    steps.add(step)
    steps.add(depending)



queue = deque([(step, n_cost + 1 + (ord(step) - ord('A'))) for step in filter(lambda x: not x in deps, sorted(steps))])

string = ""
workers = n_workers
seconds = 0
progress = []

while len(queue) > 0 or len(progress) > 0:
    for i in range(len(progress)):
        progress[i]['cost'] -= 1

    for p in progress:
        step = p['step']
        cost = p['cost']

        if cost == 0:
            progress.remove(p)
            string += step
            workers += 1

            for dep in sorted(deps):
                if step in deps[dep]:
                    deps[dep].remove(step)
                    if len(deps[dep]) == 0:
                        queue.append((dep, n_cost + 1 + (ord(dep) - ord('A'))))

    while workers > 0 and len(queue) > 0:
        step, cost = queue.popleft()
        progress.append({'step': step, 'cost': cost})
        workers -= 1

    print seconds, [p['step'] for p in progress], string
    seconds += 1

print seconds - 1, string
