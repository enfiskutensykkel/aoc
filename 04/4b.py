#!/usr/bin/env python

import re

def sorter(x, y):
    if x[1] > y[1]:
        return -1
    elif y[1] > x[1]:
        return 1

    return -1 if x[0] < y[0] else 1

alphabeth = "abcdefghijklmnopqrstuvwxyz"

def rotate(letter, sector):
    index = 0
    for l in alphabeth:
        if letter == l:
            break
        index += 1

    return alphabeth[(index + sector) % len(alphabeth)]

rooms = []

for name, sector, checksum in re.findall(r'([a-z-]+)([0-9]+)\[([^\]]+)\]\n', open('input').read()):
    letters = {}

    for letter in checksum:
        letters[letter] = 0

    for letter in name:
        if not letters.has_key(letter):
            letters[letter] = 0
        letters[letter] += 1

    del letters['-']

    counts = [(l, c) for l, c in letters.iteritems()]
    counts.sort(sorter)

    is_real = True
    for i, letter in enumerate(checksum):
        if letter != counts[i][0]:
            is_real = False
            break

    if is_real:
        real_name = ""
        for letter in name:
            if letter != '-':
                real_name += rotate(letter, int(sector))
            else:
                real_name += ' '

        rooms.append((real_name, int(sector)))

for name, sector in sorted(rooms, key=lambda x: x[1]):
    print sector, name
