#!/usr/bin/env python3
from sys import stdin


def next_step(width, grid, position, direction):
    y = position // width
    x = position % width
    dx, dy = {'N': (0, -1),
              'E': (1, 0),
              'S': (0, 1),
              'W': (-1, 0)}[direction]

    nx = x + dx
    ny = y + dy

    if 0 <= nx and nx < width and 0 <= ny and ny < len(grid) // width:
        return ny * width + nx

    return None


def neighbors(width, grid, position, direction):

    tile = grid[position]

    steps = []
    match (tile, direction):
        case ('-', 'E') | ('-', 'W') | ('|', 'N') | ('|', 'S'):
            npos = next_step(width, grid, position, direction)
            if npos is not None:
                steps.append((npos, direction))

        case ('-', 'N') | ('-', 'S'):
            npos = next_step(width, grid, position, 'E')
            if npos is not None:
                steps.append((npos, 'E'))

            npos = next_step(width, grid, position, 'W')
            if npos is not None:
                steps.append((npos, 'W'))

        case ('|', 'E') | ('|', 'W'):
            npos = next_step(width, grid, position, 'N')
            if npos is not None:
                steps.append((npos, 'N'))

            npos = next_step(width, grid, position, 'S')
            if npos is not None:
                steps.append((npos, 'S'))

        case ('/', 'N'):
            npos = next_step(width, grid, position, 'E')
            if npos is not None:
                steps.append((npos, 'E'))

        case ('/', 'E'):
            npos = next_step(width, grid, position, 'N')
            if npos is not None:
                steps.append((npos, 'N'))

        case ('/', 'W'):
            npos = next_step(width, grid, position, 'S')
            if npos is not None:
                steps.append((npos, 'S'))

        case ('/', 'S'):
            npos = next_step(width, grid, position, 'W')
            if npos is not None:
                steps.append((npos, 'W'))

        case ('\\', 'N'):
            npos = next_step(width, grid, position, 'W')
            if npos is not None:
                steps.append((npos, 'W'))

        case ('\\', 'E'):
            npos = next_step(width, grid, position, 'S')
            if npos is not None:
                steps.append((npos, 'S'))

        case ('\\', 'W'):
            npos = next_step(width, grid, position, 'N')
            if npos is not None:
                steps.append((npos, 'N'))

        case ('\\', 'S'):
            npos = next_step(width, grid, position, 'E')
            if npos is not None:
                steps.append((npos, 'E'))

        case _:
            npos = next_step(width, grid, position, direction)
            if npos is not None:
                steps.append((npos, direction))

    return steps


def bfs(width, grid, start, direction):
    q = []
    visited = set()

    visited.add((start, direction))
    q.append((start, direction))

    energized = set()

    while len(q) > 0:
        u, ud = q.pop(0)
        energized.add(u)

        for v, vd in neighbors(width, grid, u, ud):
            if (v, vd) not in visited:
                visited.add((v, vd))
                q.append((v, vd))

    return len(energized)


data = stdin.read().strip()
width = data.index('\n')
grid = [c for r in data.splitlines() for c in r]
height = len(grid) // width


print(bfs(width, grid, 0, 'E'))

# A smarter solution would be to do dijkstra's but meh

max_energized = 0
for i in range(width):
    n = bfs(width, grid, i, 'S')
    max_energized = max(max_energized, n)

    m = bfs(width, grid, (height - 1) * width + i, 'N')
    max_energized = max(max_energized, m)

for j in range(height):
    n = bfs(width, grid, width * j, 'E')
    max_energized = max(max_energized, n)

    m = bfs(width, grid, (width * j) + (width - 1), 'W')
    max_energized = max(max_energized, m)

print(max_energized)
