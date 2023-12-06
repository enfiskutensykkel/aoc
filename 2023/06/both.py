#!/usr/bin/env python3
import re
import sys

# Part 1

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

times, distances = ([int(x) for x in re.findall(r"\d+", line)]
                    for line in sys.stdin.read().strip().split("\n"))

p = 1
for t, d in zip(times, distances):
    ways = 0
    for i in range(1, t):
        distance = i * (t - i)
        if distance > d:
            ways += 1
    p *= ways

print(p)


# Part 2
time = int("".join(str(x) for x in times))
distance = int("".join(str(x) for x in distances))

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

print(time - h*2 -1)
