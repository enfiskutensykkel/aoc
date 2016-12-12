#!/usr/bin/env python

regs = {
        'a': 0,
        'b': 0,
        'c': 1, # 0 for part 1
        'd': 0
        }

data = open('input').readlines()
line = 0

while line < len(data):
    inst = data[line].strip().split(' ')

    if inst[0] == 'cpy':
        x = inst[1]
        y = inst[2]

        if x in regs:
            regs[y] = regs[x]
        else:
            regs[y] = int(x)

    elif inst[0] == 'inc':
        regs[inst[1]] += 1
    elif inst[0] == 'dec':
        regs[inst[1]] -= 1
    elif inst[0] == 'jnz':
        reg = inst[1]
        if reg in regs and regs[reg] != 0:
            line += int(inst[2])
            continue
        elif not reg in regs:
            line += int(inst[2])
            continue

    line += 1

print regs
