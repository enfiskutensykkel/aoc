#!/usr/bin/env python

import re

class Program(object):
    def __init__(self, identifier):
        self._id = identifier
        self.pipes = set()

    def add_pipe(self, program):
        self.pipes.add(program)
        program.pipes.add(self)

    def __str__(self):
        return str(self._id)

    def __repr__(self):
        return str(self)

    def connected(self, target, visited=None):
        if self == target:
            return True

        if visited == None:
            visited = set()

        if self in visited:
            return False

        visited.add(self)
        for v in self.pipes:
            if not v in visited:
                connected = v.connected(target, visited)
                if connected:
                    return True

        return False


    def group(self, visited):
        if self in visited:
            return

        visited.add(self)
        for v in self.pipes:
            if not v in visited:
                v.group(visited)



#data = """0 <-> 2
#1 <-> 1
#2 <-> 0, 3, 4
#3 <-> 2, 4
#4 <-> 2, 3, 6
#5 <-> 6
#6 <-> 4, 5""".split('\n')
data = open('input').readlines()


programs = {}
for line in data:
    progs = re.findall(r'(\d+)', line)

    identifier = int(progs[0])

    if not identifier in programs:
        programs[identifier] = Program(identifier)

    program = programs[identifier]

    for p in progs[1:]:
        identifier = int(p)
        if not identifier in programs:
            programs[identifier] = Program(identifier)

        program.add_pipe(programs[identifier])


target = programs[0]
connected = set()
sets = []

for program in programs.values():
    if program.connected(target):
        connected.add(program)

    group = set()
    program.group(group)

    if not group in sets:
        sets.append(group)

print len(connected)
print len(sets)
