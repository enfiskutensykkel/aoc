#!/usr/bin/env python

import hashlib

def next_index(puzzle, index):
    while True:
        h = hashlib.md5(puzzle + str(index)).hexdigest()

        if h[:5] == "00000":
            return index + 1, int(h[5], 16), h[6]

        index += 1


puzzle = "abbhdwsy"
#puzzle = "abc"
password = {}
i = 0

while len(password) < 8:
    i, p, c = next_index(puzzle, i)

    if p < 8 and not p in password:
        password[p] = c
        print password

print "".join(password.values())
