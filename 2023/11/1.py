#!/usr/bin/env python3
from sys import stdin


def manhattan(w, h, v, u, xf, yf):
    ux, uy = u % w, u // w
    vx, vy = v % w, v // w

    ux += 1000000 * xf
    vx += 1000000 *xf

    uy += 1000000 * yf
    vy += 1000000 * yf

    dx = abs(ux - vx)
    dy = abs(uy - vy)

    return dx + dy


def expandcols(grid):
    n = len(grid[0])
    col = 0
    factor = 0

    while col < n:
        for row in grid:
            if row[col] == '#':
                break
        else:
            #for row in range(len(grid)):
            #    grid[row].insert(col, '.')

            #col += 1
            #n += 1
            factor += 1

        col += 1
    return factor


def expandrows(grid):
    n = len(grid)
    m = len(grid[0])
    row = 0
    factor = 0

    while row < n:
        for c in grid[row]:
            if c == '#':
                break
        else:
            #grid.insert(row, '.' * m)
            #n += 1
            #row += 1
            factor += 1

        row += 1
    return factor


def print_grid(grid):
    for r in grid:
        print("".join(r))

grid = []
for line in stdin.read().strip().split("\n"):
    grid.append([c for c in line])

xfac = expandcols(grid)
yfac = expandrows(grid)

w, h = len(grid[0]), len(grid)
graph = [grid[r][c] for r in range(len(grid)) for c in range(len(grid[r]))]

nodes = set()
for i in range(len(graph)):
    if graph[i] == '#':
        nodes.add(i)

pairs = set()
for v in nodes:
    for u in nodes:
        if v != u:
            pairs.add((min(v, u), max(v, u)))

dists = []
for v, u in pairs:
    dist = manhattan(w, h, v, u, xfac, yfac)
    dists.append(dist)

print(sum(dists))

