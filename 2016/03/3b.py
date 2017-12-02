#!/usr/bin/env python

possible = 0

a_group = []
b_group = []
c_group = []

triangles = []

for line in open('input').readlines():
    a, b, c = (int(x) for x in line.split())

    a_group.append(a)
    b_group.append(b)
    c_group.append(c)

    if len(a_group) == 3:
        triangles.append(sorted(a_group))
        triangles.append(sorted(b_group))
        triangles.append(sorted(c_group))

        a_group = []
        b_group = []
        c_group = []

for a, b, c in triangles:
    if a + b > c:
        possible += 1

print possible

