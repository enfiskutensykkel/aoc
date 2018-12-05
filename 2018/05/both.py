#!/usr/bin/env python

def collapse(polymer):
    i = 0
    while i < len(polymer) - 1:
        a = ord(polymer[i])
        b = ord(polymer[i+1])

        if abs(a - b) == 32:
            polymer = polymer[:i] + polymer[i+2:]
            i = i - 1 if i > 0 else 0
        else:
            i += 1

    return i + 1



polymer = open('input').read().strip()
#polymer = "dabAcCaCBAcCcaDA"

ch = None
n = collapse(polymer)

print n

for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    l = collapse(polymer.replace(c, '').replace(chr(ord(c) + 32), ''))
    if l < n:
        n = l
        ch = c

print ch, n
