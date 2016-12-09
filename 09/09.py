#!/usr/bin/env python

import re
import sys


def decompress(s, recursive):
    pattern = re.compile(r'\((?P<length>\d+)x(?P<repeat>\d+)\)')
    decompressed = ""

    pos = 0

    while pos < len(s):
        match = pattern.match(s[pos:])

        if match:
            pos = pos + match.end()

            length = int(match.group('length'))
            repeat = int(match.group('repeat'))

            t = s[pos:pos+length] * repeat
            decompressed += decompress(t, True) if recursive else t
            pos += length

        else:
            decompressed += s[pos:pos+1]
            pos += 1

    return decompressed


def decompress_r(s):
    pattern = re.compile(r'\((?P<length>\d+)x(?P<repeat>\d+)\)')
    decompressed = 0

    pos = 0

    while pos < len(s):
        match = pattern.match(s[pos:])

        if match:
            pos = pos + match.end()

            length = int(match.group('length'))
            repeat = int(match.group('repeat'))

            t = s[pos:pos+length] * repeat
            decompressed += decompress_r(t)
            pos += length

        else:
            decompressed += 1
            pos += 1

    return decompressed



testcases = {
        'ADVENT': 'ADVENT',
        'A(1x5)BC': 'ABBBBBC',
        '(3x3)XYZ': 'XYZXYZXYZ',
        'A(2x2)BCD(2x2)EFG': 'ABCBCDEFEFG',
        '(6x1)(1x3)A': '(1x3)A',
        'X(8x2)(3x3)ABCY': 'X(3x3)ABC(3x3)ABCY',
        }

for testcase, expected in testcases.items():
    decompressed = decompress(testcase, False)

    print "PASS" if decompressed == expected else "FAIL",
    print testcase,
    print expected,
    print decompressed

print
print decompress('X(8x2)(3x3)ABCY', True) == 'XABCABCABCABCABCABCY'
print decompress_r('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
print decompress_r('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

print
print len(decompress(open('input').read().strip(), False))
print decompress_r(open('input').read().strip())
