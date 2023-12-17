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


def manhattan(width, v, u):
    ux, uy = u % width, u // width
    vx, vy = v % width, v // width

    dx = abs(ux - vx)
    dy = abs(uy - vy)

    return dx + dy



def heuristic(grid, width, v, u):
    m = manhattan(width, v, u)
    return m #+ grid[v]


def direction(width, curr, prev):
    px, py = prev % width, prev // width
    cx, cy = curr % width, curr // width
    dx = cx - px
    if dx > 0:
        return '>'
    elif dx < 0:
        return '<'
    dy = cy - py
    if dy > 0:
        return '^'
    elif dy > 1:
        return 'V'
    return None

def neighbors(width, height, u):
    d = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    x, y = u % width, u // width

    v = []
    for dx, dy in d:
        nx = x + dx
        ny = y + dy

        if (0 <= nx and nx < width
            and 0 <= ny and ny < height):
            v.append(ny *width + nx)

    return v


def astar(grid, width, start_point, exit_point):
    height = len(grid) // width

    g_costs = {}
    f_costs = {}
    rpath = {}

    infinity = width * height * 9 + 1

    for i in range(len(grid)):
        rpath[i] = None
        g_costs[i] = infinity
        f_costs[i] = infinity

    closed_list = set()
    open_list = minheap()

    f_costs[start_point] = heuristic(grid, width, exit_point, start_point)
    g_costs[start_point] = 0
    open_list.insert(start_point, f_costs[start_point])

    while len(open_list) > 0:
        u = open_list.remove()

        if u == exit_point:
            return rpath, g_costs

        # don't do the dijkstra
        closed_list.add(u)

        for v in neighbors(width, height, u):

            if v in closed_list:
                continue

            tentative = g_costs[u] + grid[v]

            if tentative < g_costs[v]:
                rpath[v] = u
                g_costs[v] = tentative
                f_costs[v] = g_costs[v] + heuristic(grid, width, v, u)

                open_list.insert(v, f_costs[v])

    return rpath, g_costs


def dijkstra(grid, width, s, t):
    dist = {}
    prev = {}

    height = len(grid) // width
    infinity = width * height * 9 + 1

    q = minheap()
    for v in range(width * height):
        for d in "^<>v":
            for i in range(1, 3):
                if v != s:
                    dist[(v, d, i)] = infinity
                    prev[(v, d, i)] = None

    #dist[(s, None, 0)] = 0
    #prev[(s, None, 0)] = s
    dist[s] = 0
    prev[s] = None
    q.insert((s, None, 0), 0)

    while len(q) > 0:
        u, ud, uc = q.remove()

        for v in neighbors(width, height, u):

            vd = direction(width, v, u)

            #alt = dist[(u, ud, uc)] + grid[v]

            if alt < dist[v]:
                prev[v] = u
                dist[v] = alt

                #uv = direction(width, v, u)

                q.insert(v, alt)

    return prev, dist


def print_grid(grid, width):
    for row in range(len(grid) // width):
        for col in range(width):
            if grid[row * width + col] >= 0:
                print(grid[row * width + col], end="")
            else:
                print('#', end="")
        print()


indata = stdin.read().strip()
width = indata.index('\n')
grid = [int(c) for line in indata.splitlines() for c in line]

#path, scores = astar(grid, width, 0, len(grid) - 1)
path, scores = dijkstra(grid, width, 0, len(grid) - 1)

print(scores[len(grid)-1])

p = len(grid) - 1
while p != 0:
    grid[p] = -1
    p = path[p]

print_grid(grid, width)
