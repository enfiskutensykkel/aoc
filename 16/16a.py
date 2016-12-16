#!/usr/bin/env python

def step(data):
    a = data
    b = ''.join(map(lambda x: '1' if x == '0' else '0',  data[::-1]))
    return a + '0' + b


def checksum(data):
    while len(data) % 2 == 0:
        csum = ""
        for i in xrange(0, len(data), 2):
            p, q = data[i:i+2]
            csum += str(int(p == q))
        data = csum
    return data


target = 272
data = "10010000000110000"

while len(data) < target:
    data = step(data)

print checksum(data[:target])
