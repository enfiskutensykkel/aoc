#!/usr/bin/env python

def redistribute(banks):
    hi = 0

    for i in range(1, len(banks)):
        if banks[i] > banks[hi]:
            hi = i

    blocks = banks[hi]
    banks[hi] = 0
    bank = hi

    while blocks > 0:
        bank = (bank + 1) % len(banks)
        banks[bank] += 1
        blocks -= 1


#banks = [0, 2, 7, 0]
banks = [int(x) for x in open('input').read().split()]
states = {}
cycles = 0

while not tuple(banks) in states:
    states[tuple(banks)] = 1
    cycles += 1

    redistribute(banks)

print cycles

cycles = 0
while not tuple(banks) in states or states[tuple(banks)] != 2:
    states[tuple(banks)] += 1
    cycles += 1

    redistribute(banks)

print cycles
