#!/usr/bin/env python3
from sys import stdin
import re


def manhattan(v, u):
    ux, uy = u
    vx, vy = v

    dx = abs(ux - vx)
    dy = abs(uy - vy)

    return dx + dy


def shoelace_area(points):
    area = 0

    n = len(points)
    j = n - 1

    for i in range(n):
        xi, yi = points[i]
        xj, yj = points[j]
        area += (xj + xi) * (yj - yi)

        j = i

    return abs(area // 2)


def total_length(points):

    total = 0

    j = 0
    for i in range(1, len(points)):
        total += manhattan(points[i], points[j])
        j = i

    return total


x = 0
y = 0

x2 = 0
y2 = 0

directions = {'R': (1, 0),
              'U': (0, -1),
              'D': (0, 1),
              'L': (-1, 0)}

directions2 = [(1, 0), (0, 1), (-1, 0), (0, -1)]

points = [(0, 0)]

points2 = [(0, 0)]


width = 0
width2 = 0
height = 0
height2 = 0

expr = re.compile(r"^([RDLU])\s+(\d+)\s+\(#([0-9a-f]{6})\)$")
for line in stdin.read().strip().splitlines():

    m = expr.search(line)
    direction, length, rgb = m.groups()

    length = int(length)

    dx, dy = directions[direction]

    x += dx * length
    y += dy * length

    points.append((x, y))

    if x > width:
        width = x + 1

    if y > height:
        height = y + 1

    length = int(rgb[:-1], base=16)
    dx, dy = directions2[int(rgb[-1])]

    x2 += dx * length
    y2 += dy * length

    points2.append((x2, y2))

length = total_length(points)
area = shoelace_area(points)

print(area + length // 2 + 1)

length = total_length(points2)
area = shoelace_area(points2)

print(area + length // 2 + 1)
