#!/usr/bin/env python3
from sys import stdin

def rotate(width, height, pattern):
    rotated = [' '] * len(pattern)

    for r in range(height):
        for c in range(width):
            rotated[c * height + r] = pattern[r * width + (width - c - 1)]
            #rotated[c * height + (height - r - 1)] = pattern[r * width + c]

    return rotated

def reflection(width, height, pattern, smudge):
    for line in range(width-1):

        lcol = line
        rcol = line + 1

        reflecting = True
        smudged = not smudge
        differences = 0
        while 0 <= lcol and rcol < width:

            for row in range(height):
                if pattern[row * width + lcol] != pattern[row * width + rcol]:
                    if smudged:
                        reflecting = False
                        break
                    smudged = True

            if not reflecting:
                break

            lcol -= 1
            rcol += 1

        if reflecting and (not smudge or smudged):
            return line

    return None

part1_total = 0
part2_total = 0
for pattern in stdin.read().strip().split("\n\n"):
    width = pattern.index("\n")

    grid = [c for line in pattern.splitlines() for c in line]
    height = len(grid) // width

    vline = reflection(width, height, grid, False)

    if vline is None:
        rotated = rotate(width, height, grid)
        hline = reflection(height, width, rotated, False)
        part1_total += (hline + 1) * 100
    else:
        part1_total += (vline + 1)

    vline2 = reflection(width, height, grid, True)

    if vline2 is None:
        rotated = rotate(width, height, grid)
        hline2 = reflection(height, width, rotated, True)
        part2_total += (hline2 + 1) * 100
    else:
        part2_total += (vline2 + 1)


print(part1_total)
print(part2_total)
