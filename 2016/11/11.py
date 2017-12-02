#!/usr/bin/env python
import re

def create_map(data):
    slots = {}
    slot = 0
    for line in data:
        for g in re.findall(r'(\w+) generator', line):
            if not g in slots:
                slots[g] = slot
                slot += 2

    floors = []
    for line in data:
        floor = [None for i in range(slot)]

        for g in re.findall(r'(\w+) generator', line):
            floor[slots[g]] = g[0] + 'g'

        for m in re.findall(r'(\w+)-compatible', line):
            floor[slots[m]+1] = m[0] + 'm'

        floors.append(floor)

    return floors


class StateMachine(object):
    def __init__(self, floors):
        self.floors = floors
        self.elevator = 0

    def print_map(self):
        for level in xrange(len(self.floors), 0, -1):
            print level,

            if self.elevator == level-1:
                print 'e',
            else:
                print '.',

            for item in self.floors[level-1]:
                if item:
                    print item,
                else:
                    print "..",

            print
        print

    def is_solved(self):
        for i in self.floors[3]:
            if i is None:
                return False
        return True

    def is_paired(self, floor, slot):
        return self.floors[floor][slot // 2 + 1] and self.floors[floor][slot // 2 + 2]

    def is_valid(self, floor):
        unshielded = 0
        generators = 0
        for slot, item in enumerate(self.floors[floor]):
            if item:
                if slot % 2 == 0:
                    generators += 1
                else:
                    unshielded += not self.is_paired(floor, slot)
        return generators == 0 or unshielded == 0

    def move_up(self, slot):
        pass






floors = create_map(open('test').readlines())

sm = StateMachine(floors)
sm.print_map()
