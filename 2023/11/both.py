#!/usr/bin/env python3
from sys import stdin


def manhattan(v, u):
    ux, uy = u
    vx, vy = v

    dx = abs(ux - vx)
    dy = abs(uy - vy)

    return dx + dy


def scan(grid, expand):
    x_factor = 0
    y_factor = 0

    expand -= 1
    nodes = set()

    for y in range(len(grid)):
        for i in range(len(grid[y])):
            if grid[y][i] == '#':
                break
        else:
            y_factor += expand
            continue

        x_factor = 0
        for x in range(len(grid[y])):
            for i in range(len(grid)):
                if grid[i][x] == '#':
                    break
            else:
                x_factor += expand
                continue

            if grid[y][x] == '#':
                nodes.add((x + x_factor, y + y_factor))

    return nodes


grid = []
for line in stdin.read().strip().split("\n"):
    grid.append([c for c in line])

for expand in [2, 1000000]:
    nodes = scan(grid, expand)

    pairs = set()
    for v in nodes:
        for u in nodes:
            if v != u:
                pairs.add((min(v, u), max(v, u)))

    dists = []
    for v, u in pairs:
        dist = manhattan(v, u)
        dists.append(dist)

    print(sum(dists))
