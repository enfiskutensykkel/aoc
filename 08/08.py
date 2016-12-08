#!/usr/bin/env python
import re

W = 7
H = 3
inputfile = 'test'
#W = 50
#H = 6
#inputfile = 'input'

def rect(screen, x, y):
    for j in xrange(y):
        for i in xrange(x):
            screen[j][i] = '#'


def rotate_col(screen, x, n):
    # inefficient but easy
    for k in xrange(n):
        top = screen[-1][x]

        for y in xrange(H - 1, 0, -1):
            screen[y][x] = screen[y - 1][x]

        screen[0][x] = top


def rotate_row(screen, y, n):
    # inefficient but easy
    for k in xrange(n):
        right = screen[y][-1]

        for x in xrange(W - 1, 0, -1):
            screen[y][x] = screen[y][x - 1]

        screen[y][0] = right


def printscreen(screen):
    for line in screen:
        print "".join(line)
    print


screen = []

for y in xrange(H):
    line = []
    for x in xrange(W):
        line.append('.')
    screen.append(line)

for line in open(inputfile).readlines():
#for line in open('test').readlines():
    instruction, args = line.strip().split(' ', 1)

    if instruction == 'rect':
        rect(screen, *(int(x) for x in args.split('x')))

    elif instruction == 'rotate':
        s = re.match(r'(?P<what>column|row) (x|y)=(?P<pos>\d+) by (?P<by>\d+)', args)

        what = s.group('what')
        pos = int(s.group('pos'))
        by = int(s.group('by'))

        if what == 'row':
            rotate_row(screen, pos, by)

        elif what == 'column':
            rotate_col(screen, pos, by)

    printscreen(screen)


#printscreen(screen)
print sum(map(lambda x: x == '#', [x for y in screen for x in y]))
