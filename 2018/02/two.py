#!/usr/bin/env python

#words = [
#        'abcde',
#        'fghij',
#        'klmno',
#        'pqrst',
#        'fguij',
#        'axcye',
#        'wvxyz'
#        ]

words = [line.strip() for line in open('input').readlines()]

def diff(a, b):
    s = ""
    num = 0

    for i, c in enumerate(a):
        if c == b[i]:
            s += c
            num += 1

    return num, s


for base in words:
    for comp in words:
        if base != comp:
            num, s = diff(base, comp)
            if num == len(base) - 1:
                print s
