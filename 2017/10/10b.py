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


def sparse2dense(l):
    s = ""
    for i in range(16):
        block = l[i*16:(i+1)*16]
        x = reduce(lambda e, a: e ^ a, block)
        s += "%x" % x
    return s



circ = range(256)
suffix = [17, 31, 73, 47, 23]
data = "88,88,211,106,141,1,78,254,2,111,77,255,90,0,54,205"
#lengths = [int(x) for x in data.split(",")]
lengths = [ord(x) for x in data] + suffix

pos = 0
skip = 0

for i in xrange(64):
    for length in lengths:
        s = sublist(circ, pos, length)
        insert(circ, pos, reversed(s))

        pos += length + skip
        skip += 1

print sparse2dense(circ)
