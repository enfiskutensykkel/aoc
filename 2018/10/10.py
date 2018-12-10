#!/usr/bin/env python
from __future__ import print_function
import re

#data = """position=< 9,  1> velocity=< 0,  2>
#position=< 7,  0> velocity=<-1,  0>
#position=< 3, -2> velocity=<-1,  1>
#position=< 6, 10> velocity=<-2, -1>
#position=< 2, -4> velocity=< 2,  2>
#position=<-6, 10> velocity=< 2, -2>
#position=< 1,  8> velocity=< 1, -1>
#position=< 1,  7> velocity=< 1,  0>
#position=<-3, 11> velocity=< 1, -2>
#position=< 7,  6> velocity=<-1, -1>
#position=<-2,  3> velocity=< 1,  0>
#position=<-4,  3> velocity=< 2,  0>
#position=<10, -3> velocity=<-1,  1>
#position=< 5, 11> velocity=< 1, -2>
#position=< 4,  7> velocity=< 0, -1>
#position=< 8, -2> velocity=< 0,  1>
#position=<15,  0> velocity=<-2,  0>
#position=< 1,  6> velocity=< 1,  0>
#position=< 8,  9> velocity=< 0, -1>
#position=< 3,  3> velocity=<-1,  1>
#position=< 0,  5> velocity=< 0, -1>
#position=<-2,  2> velocity=< 2,  0>
#position=< 5, -2> velocity=< 1,  2>
#position=< 1,  4> velocity=< 2,  1>
#position=<-2,  7> velocity=< 2, -2>
#position=< 3,  6> velocity=<-1, -1>
#position=< 5,  0> velocity=< 1,  0>
#position=<-6,  0> velocity=< 2,  0>
#position=< 5,  9> velocity=< 1, -2>
#position=<14,  7> velocity=<-2,  0>
#position=<-3,  6> velocity=< 2, -1>"""

class Point(object):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy


def print_grid(grid):
    coords = [None] * 4
    for x, y in grid:
        if coords[0] is None or x < coords[0]:
            coords[0] = x
        if coords[1] is None or x > coords[1]:
            coords[1] = x
        if coords[2] is None or y < coords[2]:
            coords[2] = y
        if coords[3] is None or y > coords[3]:
            coords[3] = y

    for y in range(coords[2], coords[3] + 1):
        for x in range(coords[0], coords[1] + 1):
            if (x, y) in prev_grid:
                print('#', end='')
            else:
                print('.', end='')
        print()


data = open('input').read()
points = []
for p, v in re.findall(r'position=<([^>]*)> velocity=<([^>]*)>', data):
    x, y = [int(m) for m in re.findall(r'-?\d+', p)]
    vx, vy = [int(m) for m in re.findall(r'-?\d+', v)]

    points.append(Point(x, y, vx, vy))

secs = 0
prev_grid = None
prev_height = None
while True:
    grid = set()

    bottom = 10**6
    top = -10**6
    for p in points:
        if p.y < bottom:
            bottom = p.y

        if p.y > top:
            top = p.y

        grid.add((p.x, p.y))
        p.update()

    height = top - bottom

    if prev_height is None or height < prev_height:
        prev_grid = grid
        prev_height = height
        secs += 1
    else:
        break

print_grid(prev_grid)
print(secs - 1)
