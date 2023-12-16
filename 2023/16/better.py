#!/usr/bin/env python3
from sys import stdin


def direction(width, curr, prev):
    px, py = prev % width, prev // width
    cx, cy = curr % width, curr // width
    dx = cx - px
    if dx > 0:
        return 'E'
    elif dx < 0:
        return 'W'
    dy = cy - py
    if dy > 0:
        return 'S'
    return 'N'


def nextpos(width, grid, curr, prev, init=None):

    if prev is not None:
        d = direction(width, curr, prev)
    else:
        d = init

    tile = grid[curr]
    dmap = {('-', 'N'): 'EW',
            ('-', 'S'): 'EW',
            ('|', 'E'): 'NS',
            ('|', 'W'): 'NS',
            ('/', 'N'): 'E',
            ('/', 'E'): 'N',
            ('/', 'W'): 'S',
            ('/', 'S'): 'W',
            ('\\','N'): 'W',
            ('\\','W'): 'N',
            ('\\','S'): 'E',
            ('\\','E'): 'S'}

    nds = dmap.get((tile, d), d)

    y = curr // width
    x = curr % width

    ndmap = {'N': (0, -1),
             'E': (1, 0),
             'S': (0, 1),
             'W': (-1, 0)}

    pos = []
    for nd in nds:
        dx, dy = ndmap[nd]

        nx = x + dx
        ny = y + dy

        if (0 <= nx and nx < width
            and 0 <= ny and ny < (len(grid) // width)):
            pos.append(ny * width + nx)

    return pos


def bfs(width, grid, p_init, d_init):
    q = [(p_init, None)]
    visited = set(q)
    energized = set()
    energized.add(p_init)

    while len(q) > 0:
        v, u = q.pop(0)
        energized.add(v)

        for w in nextpos(width, grid, v, u, init=d_init):
            if (w, v) not in visited:
                visited.add((w, v))
                q.append((w, v))

    return len(energized)


data = stdin.read().strip()
width = data.index('\n')
grid = [c for r in data.splitlines() for c in r]


print(bfs(width, grid, 3, 'S'))
