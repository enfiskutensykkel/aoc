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


def get_edges(grid, width, height, vertex, current_direction, min_dist, max_dist):
    x, y = vertex % width, vertex // width

    updown = [('^', (0, -1)), ('v', (0, 1))]
    leftright = [('<', (-1, 0)), ('>', (1, 0))]

    if current_direction is None:
        directions = updown + leftright
    else:
        directions = {'^': leftright,
                      'v': leftright,
                      '<': updown,
                      '>': updown}[current_direction]

    candidates = []
    for direction, (dx, dy) in directions:
        cost = 0

        vx = x
        vy = y

        for i in range(min_dist-1):
            vx += dx
            vy += dy

            if not (0 <= vx and vx < width and 0 <= vy and vy < height):
                break

            cost += grid[vy * width + vx]

        if not (0 <= vx and vx < width and 0 <= vy and vy < height):
            continue

        for i in range(min_dist-1, max_dist):
            vx += dx
            vy += dy

            if not (0 <= vx and vx < width and 0 <= vy and vy < height):
                break

            v = vy * width + vx
            cost += grid[v]
            candidates.append((v, direction, cost))

    return candidates


def bfs(grid, width, height, min_step, max_step):
    graph = {}

    graph[(0, None)] = get_edges(grid, width, height, 0, None, min_step, max_step)

    q = [(0, None)]

    while len(q) > 0:
        u, u_direction = q.pop(0)

        for v, direction, cost in graph[(u, u_direction)]:
            if not (v, direction) in graph:
                graph[(v, direction)] = get_edges(grid, width, height, v, direction, min_step, max_step)
                q.append((v, direction))

    return graph


def dijkstra(graph):
    dist = {}
    prev = {}

    infinity = 10000000

    for v, d in graph.keys():
        dist[(v, d)] = infinity
        prev[(v, d)] = None

    dist[(0, None)] = 0
    prev[(0, None)] = None

    q = minheap()
    q.insert((0, None), 0)

    while len(q) > 0:
        u, curr_direction = q.remove()

        for v, direction, cost in graph[(u, curr_direction)]:
            alt = dist[(u, curr_direction)] + cost

            if alt < dist[(v, direction)]:
                prev[(v, direction)] = u
                dist[(v, direction)] = alt
                q.insert((v, direction), alt)

    return prev, dist


indata = stdin.read().strip()
width = indata.index('\n')
grid = [int(c) for line in indata.splitlines() for c in line]

for min_step, max_step in [(1, 3), (4, 10)]:
    graph = bfs(grid, width, len(grid) // width, min_step, max_step)

    paths, costs = dijkstra(graph)

    min_cost = 10000000
    for (v, d), cost in costs.items():
        if v == len(grid) - 1 and cost < min_cost:
            min_cost = cost
    print(min_cost)
