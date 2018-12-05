#!/usr/bin/env python

def collapse(polymer):
    reaction = True
    while reaction:
        reaction = False

        for i in xrange(len(polymer) - 1):
            a = ord(polymer[i])
            b = ord(polymer[i + 1])

            if abs(a - b) == 32:
                reaction = True
                polymer = polymer[:i] + polymer[i + 2:]
                break

    return len(polymer)



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
