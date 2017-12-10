#!/usr/bin/env python

def sublist(l, pos, length):
    s = []
    for i in xrange(pos, pos+length):
        s.append(l[i % len(l)])
    return s


def insert(l, pos, s):
    for i in s:
        l[pos % len(l)] = i
        pos += 1


circ = range(0, 256)
data = "88,88,211,106,141,1,78,254,2,111,77,255,90,0,54,205"
lengths = [int(x) for x in data.split(",")]

pos = 0
skip = 0

while len(lengths) > 0:
    length = lengths[0]
    lengths = lengths[1:]

    s = sublist(circ, pos, length)
    insert(circ, pos, reversed(s))

    pos += length + skip
    skip += 1

print circ[0] * circ[1]
