#!/usr/bin/env python3
import re
from sys import stdin


def neighbors(w, h, graph, v):
    x, y = (v % w), (v // w)

    tile = graph[v]
    checks = {'S': {(x, y-1): "|F7",
                    (x-1, y): "-FL",
                    (x, y+1): "|JL",
                    (x+1, y): "-J7"},
              '-': {(x-1, y): "-LFS",
                    (x+1, y): "-J7S"},
              '|': {(x, y-1): "|F7S",
                    (x, y+1): "|JLS"},
              'F': {(x+1, y): "-J7S",
                    (x, y+1): "|JLS"},
              '7': {(x-1, y): "-FLS",
                    (x, y+1): "|JLS"},
              'L': {(x+1, y): "-J7S",
                    (x, y-1): "|F7S"},
              'J': {(x-1, y): "-FLS",
                    (x, y-1): "|F7S"}
              }[tile]

    u = []
    for (i, j), tiles in checks.items():
        if 0 <= i and i < w and 0 <= j and j < h:
            if graph[j * w + i] in tiles:
                u.append(j * w + i)

    return u


def bfs(w, h, graph, s):
    Q = []
    visited = set()
    visited.add(s)
    Q.append(s)

    dist = {}
    dist[s] = 0

    while len(Q) > 0:
        u = Q.pop(0)

        for v in neighbors(w, h, graph, u):
            if v not in visited:
                visited.add(v)
                Q.append(v)
                dist[v] = dist[u] + 1

    return dist[u]


def dfs(w, h, graph, s):
    S = [s]
    visited = set()
    corners = []

    while len(S) > 0:
        u = S.pop()
        x, y = u % w, u // w

        if u in visited:
            continue

        visited.add(u)

        if graph[u] in "SFJ7L":
            corners.append(u)

        for v in neighbors(w, h, graph, u):
            S.append(v)

    return corners


def shoelace_area(w, h, points):
    area = 0

    n = len(points)
    j = n - 1

    for i in range(n):
        xi, yi = points[i] % w, points[i] // w
        xj, yj = points[j] % w, points[j] // w
        area += (xj + xi) * (yj - yi)
        j = i

    return abs(area // 2)


# Parse tile map
tiles = {}
start = -1
for y, row in enumerate(stdin.read().strip().split("\n")):
    h = y + 1
    w = len(row)
    for x, tile in enumerate(row):
        tiles[y * w + x] = tile
        if tile == "S":
            start = y * w + x

# Find the main loop
max_distance = bfs(w, h, tiles, start)
print(max_distance)

# Traverse graph to find corners
points = dfs(w, h, tiles, start)

# Calculate area using shoelace formula
area = shoelace_area(w, h, points)

# Pick's theorem: subtract half the vertices
# (area + 2 - length) / 2 --> area - max_distance (which is halfway away) + 1
print(area + 1 - max_distance)
