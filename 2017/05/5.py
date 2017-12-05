#!/usr/bin/env python

instr = [int(x) for x in open("input").readlines()]
#instr = [0, 3, 0, 1, -3]

steps = 0
pos = 0
while pos < len(instr):
    jump = instr[pos]
    #instr[pos] += 1 # part 1
    instr[pos] += 1 if instr[pos] < 3 else -1 # part 2
    pos += jump
    steps += 1

print steps
