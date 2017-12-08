#!/usr/bin/env python

import re


def condition(a, b, operator):
    return eval('{} {} {}'.format(a, operator, b))

expr = re.compile(r'(?P<reg>\w+) (?P<action>dec|inc) (?P<val>-?\d+) if (?P<creg>\w+) (?P<operator>>|<|==|>=|<=|!=) (?P<cval>-?\d+)')

#instrs = [
#        "b inc 5 if a > 1",
#        "a inc 1 if b < 5",
#        "c dec -10 if a >= 1",
#        "c inc -20 if c == 10"
#        ]
instrs = open('input').readlines()

regs = {}
hi = 0

for instr in instrs:
    s = re.search(expr, instr)
    reg = s.group('reg')
    creg = s.group('creg')

    if not reg in regs:
        regs[reg] = 0
    if not creg in regs:
        regs[creg] = 0

    val = int(s.group('val'))
    if s.group('action') == 'dec':
        val *= -1

    cval = int(s.group('cval'))

    if condition(regs[creg], cval, s.group('operator')):
        regs[reg] += val
        if regs[reg] > hi:
            hi = regs[reg]

print max(regs.values())
print hi
