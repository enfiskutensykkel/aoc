#!/usr/bin/env python3

test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def is_part_number(x, y):
    start_x = x
    end_x = x + len(str(numbers[(x, y)]))

    for xi in range(start_x - 1, end_x+1):
        yi = y - 1
        if yi >= 0 and xi >= 0 and xi < width:
            if grid[(xi, yi)] != '.':
                return True

    for xi in (start_x - 1, end_x):
        yi = y
        if xi >= 0 and xi < width:
            if grid[(xi, yi)] != '.':
                return True

    for xi in range(start_x - 1, end_x+1):
        yi = y + 1
        if yi < height and xi >= 0 and xi < width:
            if grid[(xi, yi)] != '.':
                return True

    return False

grid = {}
gears = {}
numbers = {}

for y, line in enumerate(open("input.txt").readlines()):
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
            numbers[(start_x, y)] = number
            number = 0
            start_x = -1
        elif v == 42:
            gears[(x, y)] = c


s = 0
for coord, number in numbers.items():
    if is_part_number(*coord):
        s += number
    else:
        print(number)
print(s)

#for coord in gears.keys():
    #if is_gear(*coord):

