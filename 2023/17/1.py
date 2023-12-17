#!/usr/bin/env python3
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


class crucible:
    def key(self):
        return (self.position, self.direction, self.steps)

    def __repr__(self):
        return repr(self.key())

    def __init__(self, grid, width, height, position, direction, steps):
        self.position = position
        self.cost = grid[position]
        self.direction = direction
        self.steps = steps

        neighbours = {'^': (0, -1),
                     'v': (0, 1),
                     '<': (-1, 0),
                     '>': (1, 0)}

        opposite = {'^': 'v',
                    'v': '^',
                    '<': '>',
                    '>': '<',
                    None: None}

        x = self.position % width
        y = self.position // width

        self.neighbours = {}

        for direction, (dx, dy) in neighbours.items():
            if direction == opposite[self.direction]:
                # can't go in reverse
                continue

            steps = 1
            if direction == self.direction:
                steps = self.steps + 1

            if direction == self.direction and steps > 3:
                # can't go more than 3 steps in the same direction
                continue

            vx = dx + x
            vy = dy + y
            v = vy * width + vx

            if (0 <= vx and vx < width
                and 0 <= vy and vy < height):
                self.neighbours[direction] = (v, direction, steps)


def bfs(grid, width, height, s):
    graph = {}
    graph[s.key()] = s
    queue = [s]

    while len(queue) > 0:
        u = queue.pop(0)

        for v, direction, steps in u.neighbours.values():
            if not (v, direction, steps) in graph:
                v = crucible(grid, width, height, v, direction, steps)
                graph[v.key()] = v
                queue.append(v)

    return graph


def dijkstra(graph, s):
    dist = {}
    prev = {}

    height = len(grid) // width
    infinity = width * height * 9 + 1

    q = minheap()
    for v in graph.keys():
        dist[v] = infinity
        prev[v] = v

    dist[s.key()] = 0
    prev[s.key()] = s
    q.insert(s, 0)

    while len(q) > 0:
        u = q.remove()

        for vkey in u.neighbours.values():
            v = graph[vkey]

            alt = dist[u.key()] + v.cost
            if alt < dist[vkey]:
                prev[vkey] = u
                dist[vkey] = alt
                q.insert(v, alt)

    return prev, dist


def print_grid(grid, width, height, path, start):

    steps = {}

    while True:
        steps[start.position] = start.direction

        if path[start.key()] == start:
            break

        start = path[start.key()]

    for row in range(height):
        for col in range(width):
            v = row * width + col
            if v in steps and steps[v] is not None:
                print(steps[v], end="")
            else:
                print(grid[v], end="")
        print()


def find_minimum(grid, width, height):

    start = crucible(grid, width, height, 0, None, 0)

    graph = bfs(grid, width, height, start)

    path, scores = dijkstra(graph, start)

    minimum = width * height * 9 + 1
    l = None

    for (v, d, s), dist in scores.items():
        if v == len(grid) - 1:
            minimum = min(minimum, dist)
            l = (v, d, s)

    #print_grid(grid, width, height, path, graph[l])

    return minimum


indata = stdin.read().strip()
width = indata.index('\n')
grid = [int(c) for line in indata.splitlines() for c in line]

print(find_minimum(grid, width, len(grid) // width))

