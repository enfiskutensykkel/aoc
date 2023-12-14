#!/usr/bin/env python3
from sys import stdin

def tilt(width, grid):
    height = len(grid) // width
    for r in range(height):
        for c in range(width):
            if grid[r * width + c] == 'O':
                to_row = r

                while to_row-1 >= 0 and grid[(to_row-1) * width + c] == '.':
                    to_row -= 1

                grid[r * width + c] = '.'
                grid[to_row * width + c] = 'O'


def total_load(width, grid):
    total = 0
    height = len(grid) // width
    for r in range(height):
        for c in range(width):
            if grid[r * width + c] == 'O':
                total += height - r

    return total


def rotate(width, grid):
    rotated = [' '] * len(grid)

    height = len(grid) // width
    for r in range(height):
        for c in range(width):
            rotated[c * height + (height - r - 1)] = grid[r * width + c]

    for i, c in enumerate(rotated):
        grid[i] = c


def spin_cycle(width, grid):
    tilt(width, grid) # north

    rotate(width, grid)
    tilt(len(grid) // width, grid) # west

    rotate(len(grid) // width, grid)
    tilt(width, grid) # south

    rotate(width, grid)
    tilt(len(grid) // width, grid) # east

    rotate(len(grid) // width, grid) # orient back to north


indata = stdin.read().strip()
width = indata.index("\n")
grid = [c for line in indata.splitlines() for c in line]

cycles = 1000000000
seen = {}
loads = []

for cycle in range(cycles):
    k = hash("".join(grid))
    if k in seen:
        break

    spin_cycle(width, grid)
    loads.append(total_load(width, grid))
    seen[k] = cycle

cycle_start = seen[k]
cycle_length = cycle - cycle_start

offset = (cycles - cycle_start) % (cycle_length)

print(loads[cycle_start + offset - 1])
