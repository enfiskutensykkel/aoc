#!/usr/bin/env python

data = 265149


def ring(x):
    return (2 * x + 1) ** 2


def length(r):
    if r == 0:
        return 1

    return length(r - 1) + 2


def position(n):
    r = 0
    last = 1
    x, y = 0, 0

    while n > last:
        r += 1
        last = ring(r)
        x += 1
        y += 1

    wall = length(r)

    north = lambda x, y: (x, y - 1)
    west = lambda x, y: (x - 1, y)
    south = lambda x, y: (x, y + 1)
    east = lambda x, y: (x + 1, y)

    directions = [north, west, south, east]

    for i in range((wall - 1) * 4):
        if n == last:
            return x, y

        last -= 1
        x, y = directions[i / (wall - 1)](x, y)

    return 0, 0


def generate_ring(x):
    if x == 0:
        return [1]

    return range(ring(x - 1) + 1, ring(x) + 1)


spiral = {}
spiral[(0, 0)] = 1

cells = {}
for i, v in enumerate([1, 1, 2, 4, 5, 10, 11, 23, 25]):
    cells[i+1] = v

for k, v in cells.iteritems():
    y, x = position(k)
    spiral[(x, y)] = v


def calculate_cell(n):
    y, x = position(n)
    if (x, y) in spiral:
        return spiral[(x, y)]

    calculate_cell(n - 1)

    value = 0
    for ix in (-1, 0, 1):
        for iy in (-1, 0, 1):
            if (x+ix, y+iy) in spiral:
                value += spiral[(x+ix, y+iy)]

    spiral[(x, y)] = value
    return value



# I don't know why (x, y) is reversed :(
y, x = position(data)
print abs(x) + abs(y)


highest = 1
n = 1
while highest <= data:
    n += 1
    highest = calculate_cell(n)

print highest

