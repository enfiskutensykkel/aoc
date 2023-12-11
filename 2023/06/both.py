#!/usr/bin/env python3
import re
import sys

# x-axis = hold time
# y-axis = race length-1
#
#       0
#     0 1 0
#    0 2 2 0
#   0 3 4 3 0
#  0 4 6 6 4 0
# 0 5 8 9 8 5 0
#0 6 a c c a 6 0

def ways(time, distance):
#    ways = 0
#    for i in range(1, time):
#        d = i * (time - i)
#        if d > distance:
#            ways += 1
#    return ways
    h = time // 2
    l = 1
    while l < h:
        i = (l + h) // 2
        d = i * (time - i)

        if d > distance:
            h = i - 1
        elif d < distance:
            l = i + 1
        else:
            break

    d = h * (time - h)
    while d > distance:
        h -= 1
        d = h * (time - h)

    return (time - h*2 - 1)

times, distances = ([int(x) for x in re.findall(r"\d+", line)]
                    for line in sys.stdin.read().strip().split("\n"))

p = 1
for t, d in zip(times, distances):
    w = ways(t, d)
    p *= w

print(p)

time = int("".join(str(x) for x in times))
distance = int("".join(str(x) for x in distances))
print(ways(time, distance))
