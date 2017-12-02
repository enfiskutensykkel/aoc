#!/usr/bin/env python

data = open("input").readlines()
#data = ["5 9 2 8", "9 4 7 3", "3 8 6 5"]

checksum = 0

for row in data:
    values = [int(x) for x in row.split()]

    for i, a in enumerate(values):
        for b in values[i+1:]:
            dividend = max(a, b)
            divisor = min(a, b)

            if dividend % divisor == 0:
                checksum += dividend / divisor
                break

print checksum
