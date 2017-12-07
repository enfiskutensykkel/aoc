#!/usr/bin/env python

import re

class Program(object):

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.parents = []

    def add_parent(self, parent):
        self.parents.append(parent)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def count(self):
        count = 1
        for parent in self.parents:
            count += parent.count()
        return count

    def accumulate(self):
        weight = self.weight

        for p in self.parents:
            weight += p.accumulate()

        return weight

    def balanced(self):
        if len(self.parents) == 0:
            return self.weight

        weights = {}
        for p in self.parents:
            weights[p] = p.balanced()

        maxp = None
        minp = None
        for p, a in weights.iteritems():
            if maxp is None:
                maxp = p
            if minp is None:
                minp = p

            if weights[p] < weights[minp]:
                minp = p
            elif weights[p] > weights[maxp]:
                maxp = p

        diff = weights[maxp] - weights[minp]
        if diff != 0:
            print maxp, weights[maxp], weights[maxp] - diff, maxp.weight, maxp.weight - diff
            #print minp, minp.weight, minp.weight + diff

        return self.weight + sum(weights.values())



node_expr = re.compile(r'(?P<name>\w+)\s\((?P<weight>\d+)\)')
parent_expr = re.compile(r',?\s(\w+)')

data = open('input').readlines()

#data = """pbga (66)
#xhth (57)
#ebii (61)
#havc (66)
#ktlj (57)
#fwft (72) -> ktlj, cntj, xhth
#qoyq (66)
#padx (45) -> pbga, havc, qoyq
#tknk (41) -> ugml, padx, fwft
#jptl (61)
#ugml (68) -> gyxo, ebii, jptl
#gyxo (61)
#cntj (57)""".split("\n")


programs = {}
for line in data:
    m = re.search(node_expr, line)
    program = Program(m.group('name'), int(m.group('weight')))
    programs[m.group('name')] = program

for line in data:
    m = re.search(node_expr, line)
    program = programs[m.group('name')]
    for parent in re.findall(parent_expr, line):
        program.add_parent(programs[parent])

counts = {}
for program in programs.itervalues():
    counts[program] = program.count()


most = None
for program, count in counts.iteritems():
    if most is None or count > counts[most]:
        most = program

print most

most.balanced()

