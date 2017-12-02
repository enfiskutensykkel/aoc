#!/usr/bin/env python

import hashlib

def next_index(puzzle, index):
    while True:
        h = hashlib.md5(puzzle + str(index)).hexdigest()

        if h[:5] == "00000":
            return index + 1, h[5]

        index += 1


puzzle = "abbhdwsy"
#puzzle = "abc"
password = ""
i = 0

while len(password) < 8:
    i, c = next_index(puzzle, i)
    password += c
    print password
