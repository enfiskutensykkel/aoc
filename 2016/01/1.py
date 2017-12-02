#!/usr/bin/env python

x, y = 0, 0
facing = 0
locations = {(0,0): 1}

for instruction in [i.strip() for i in open("1-input.txt").read().split(",")]:

    turn = instruction[0]
    number = int(instruction[1:])

    if turn == 'R':
        facing = (facing + 90) % 360
    elif turn == 'L':
        facing = (facing - 90) % 360

    for k in xrange(number):
        if facing == 0:
            y += 1
        elif facing == 90:
            x += 1
        elif facing == 180:
            y -= 1
        elif facing == 270:
            x -= 1

        locations[(x, y)] = locations[(x, y)] + 1 if (x, y) in locations else 1

        if locations[(x, y)] > 1:
            print (x, y), abs(x) + abs(y)

print (x, y), abs(x) + abs(y)
