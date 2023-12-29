#!/usr/bin/env python3
from sys import stdin

def rotate(width, grid):
    rotated = [' '] * len(grid)

    height = len(grid) // width
    for r in range(height):
        for c in range(width):
            rotated[c * height + (height - r - 1)] = grid[r * width + c]

    for i, c in enumerate(rotated):
        grid[i] = c


def print_grid(width, grid):
    for r in range(len(grid) // width):
        for c in range(width):
            print(grid[r * width + c], end="")
        print()

indata = stdin.read().strip()
width = indata.index("\n")
grid = [c for line in indata.splitlines() for c in line]

def total_load(width, grid):
    total = 0
    height = len(grid) // width
    for r in range(height):
        for c in range(width):
            if grid[r * width + c] == 'O':
                total += height - r

    return total

print(total_load(width, grid))
#print_grid(width, grid)
#print()
#rotate(width, grid)
#print_grid(width, grid)
