#!/usr/bin/env python

def move(q, r, direction):
    coords = {
            'n': (0, -1),
            'nw': (-1, 0),
            'sw': (-1, 1),
            's': (0, 1),
            'se': (1, 0),
            'ne': (1, -1)
            }

    x, y = coords[direction]
    return q+x, r+y



#tests = ["ne,ne,ne", "ne,ne,sw,sw", "ne,ne,s,s", "se,sw,se,sw,sw"]
#path = tests[3].split(',')

path = open('input').read().strip().split(',')

x, y = 0, 0
m = 0
for step in path:
    x, y = move(x, y, step)
    n = max(abs(x), abs(y))
    m = max(m, n)

print max(abs(x), abs(y))
print m
