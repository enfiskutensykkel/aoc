#!/usr/bin/env python3
import re

digits = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
r = "|".join(digits)
expr = re.compile(rf"(?=({r}|\d))")

test = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

s = 0
for line in open("input.txt").readlines():
    d = expr.findall(line)
    first, last = d[0], d[-1]
    if first in digits:
        first = str(digits.index(first))
    if last in digits:
        last = str(digits.index(last))
    s += int(first + last)
print(s)
