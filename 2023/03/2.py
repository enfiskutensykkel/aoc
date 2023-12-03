#!/usr/bin/env python3

test = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

#test = """
#........................#.............
#........894....334.............766.817
#....228...........*...183.............
#.......*........920..*....&...........
#.....#.623..........183...28.....460..
#..148........636................*.....
#...............-.158........362..220..
#"""

def is_gear(x, y):
    n = []
    for j in range(y-1, y+2):
        if j < 0 or j > height:
            continue

        line = set()
        for i in range(x-1, x+2):
            if i < 0 or i > width:
                continue

            if (i, j) in numbers:
                line.add(numbers[(i, j)])

        for l in line:
            n.append(l)

    if len(n) == 2:
        p = 1
        for i in n:
            p *= i
        return p

    return 0


grid = {}
gears = {}
numbers = {}

duplicates = set()
real_pos = {}

for y, line in enumerate(open("input.txt").readlines()):
#for y, line in enumerate(test.strip().split()):
    height = y

    for x, c in enumerate(line):
        width = x
        grid[(x, y)] = c

    number = 0
    start_x = -1
    for x, c in enumerate(line):
        v = ord(c)
        if 48 <= v and v <= 57:
            if start_x == -1:
                start_x = x
            number = number*10 + int(c)
        elif start_x != -1:
            for i in range(start_x, x):
                numbers[(i, y)] = number
            real_pos[(start_x, y)] = number

            number = 0
            start_x = -1

        if v == 42:
            gears[(x, y)] = c

    if start_x != -1:
        real_pos[(start_x, y)] = number
        for i in range(start_x, width+1):
            numbers[(i, y)] = number

reverse = {}
for coord, num in real_pos.items():
    if num not in reverse:
        reverse[num] = []
    reverse[num].append(coord)

for num, coords in reverse.items():
    if len(coords) > 1:
        for x0, y0 in coords:
            x_range = range(x0-2, x0+3)
            y_range = range(y0-2, y0+3)

            for x1, y1 in coords:
                if x0 == x1 and y0 == y1:
                    continue

                if x1 in x_range and y1 in y_range:
                    pass

s = 0
for coord in gears:
    s += is_gear(*coord)

print(s)
