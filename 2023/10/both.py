#!/usr/bin/env python3
import re
from sys import stdin


class minheap:
    class element:
        def __init__(self, k, d):
            self.key = k
            self.element = d

    def __init__(self):
        self.elems = [None]
        self.size = 0

    def __len__(self):
        return self.size

    def percolate_up(self, idx):
        while idx // 2 > 0:
            if self.elems[idx].key < self.elems[idx // 2].key:
                tmp = self.elems[idx // 2]
                self.elems[idx // 2] = self.elems[idx]
                self.elems[idx] = tmp
            idx //= 2

    def percolate_down(self, idx):
        while (idx * 2) <= self.size:
            child = idx * 2

            if child+1 <= self.size and self.elems[child+1].key < self.elems[child].key:
                child += 1

            if self.elems[idx].key > self.elems[child].key:
                tmp = self.elems[idx]
                self.elems[idx] = self.elems[child]
                self.elems[child] = tmp

            idx = child

    def insert(self, element, key):
        self.elems.append(self.element(key, element))
        self.size += 1
        self.percolate_up(self.size)

    def remove(self):
        if self.size > 0:
            elem = self.elems[1].element
            self.elems[1] = self.elems[self.size]
            self.size -= 1
            self.elems.pop()
            self.percolate_down(1)
            return elem
        return None


def print_map(w, h, graph):
    for y in range(h):
        for x in range(w):
            print(graph[y * w + x], end="")
        print()


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


def dijkstra(w, h, graph, s):
    dist = {}
    prev = {}
    infinity = 1000000000

    q = minheap()
    dist[s] = 0
    prev[s] = s
    for v in range(w * h):
        if v != s and graph[v] != "." and len(neighbors(w, h, graph, v)) > 0:
            dist[v] = infinity
            prev[v] = None

    q.insert(s, 0)

    while len(q) > 0:
        u = q.remove()

        for v in neighbors(w, h, graph, u):
            alt = dist[u] + 1
            if alt < dist[v]:
                prev[v] = u
                dist[v] = alt
                q.insert(v, alt)

    return ({v: d for v, d in dist.items() if d < infinity},
            {v: u for v, u in prev.items() if u != None})


def flood(w, h, graph, loop, s):
    q = [s]
    visited = set()
    visited.add(s)
    area = set()

    squeezing = False

    while len(q) > 0:
        u = q.pop(0)
        x, y = (u % w), (u // w)

        if x == 0 or y == 0 or x == w-1 or y == h-1:
            return None

        search_patterns = {"|": [(0, -1), (0, 1)],
                           "-": [(-1, 0), (1, 0)],
                           None: [(0, -1), (-1, 0), (1, 0), (0, 1)]}

        search_pattern = search_patterns[None]
        if u not in loop:
            area.add(u)

        elif graph[u] in search_patterns:
            search_pattern = search_patterns[graph[u]]

        for (dx, dy) in search_pattern:
            i = x + dx
            j = y + dy
            v = j * w + i

            if v in visited:
                continue

            if u not in loop or v not in loop:
                q.append(v)
                visited.add(v)
                continue

            match (dx, dy, graph[u]):
                case 0, -1, 'L':
                    allowed_pattern = "|F"
                case 0, -1, 'J':
                    allowed_pattern = "|7"
                case 0, 1, 'F':
                    allowed_pattern = "|L"
                case 0, 1, '7':
                    allowed_pattern = "|J"
                case -1, 0, 'J':
                    allowed_pattern = "-L"
                case -1, 0, '7':
                    allowed_pattern = "-F"
                case 1, 0, 'L':
                    allowed_pattern = "-J"
                case 1, 0, 'F':
                    allowed_pattern = "-7"
                case _:
                    allowed_pattern = ""

            while 0 <= i and i < w and 0 <= j and j < h:
                v = j * w + i

                if v not in loop or not graph[v] in allowed_pattern + graph[u]:
                    break

                visited.add(v)
                q.append(v)

                i += dx
                j += dy

    return area

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
steps, paths = dijkstra(w, h, tiles, start)
print(max(steps.values()))

# Find largest area enclosed by the loop
enclosed_area = set()
for y in range(h):
    for x in range(w):
        visited = flood(w, h, tiles, paths, y * w + x)
        if visited is not None:
            for x in visited:
                tiles[x] = '@'
                enclosed_area.add(x)

print_map(w, h, tiles)
print(len(enclosed_area))
