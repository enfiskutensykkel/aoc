#!/usr/bin/env python

def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def grid_dim(coords):
    w = 0
    h = 0

    for x, y in coords:
        if x > w:
            w = x + 1

        if y > h:
            h = y + 1

    return w, h


def is_bound(p, coords):
    w, h = grid_dim(coords)
    x, y = p

    def direction(stepx, stepy):
        i = x
        j = y

        while i >= 0 and i <= w and j >= 0 and j <= h:
            if closest((i, j), coords) != p:
                return False

            i += stepx
            j += stepy

        return True

    if direction(-1, 0):
        return False

    if direction(1, 0):
        return False

    if direction(0, -1):
        return False

    if direction(0, 1):
        return False

    return True


def closest(p, coords):
    closest = None
    closest_dist = None

    for x, y in coords:
        dist = manhattan(p, (x, y))

        if closest is None or dist < closest_dist:
            closest_dist = dist
            closest = (x, y)

    for x, y in coords:
        if closest != (x, y) and manhattan(p, (x, y)) == closest_dist:
            return None

    return closest

coords = [
        (1, 1),
        (1, 6),
        (8, 3),
        (3, 4),
        (5, 5),
        (8, 9),
        ]

coords = [tuple(int(part) for part in line.split(',')) for line in open('input').readlines()]

w, h = grid_dim(coords)
g = {}
for y in xrange(h):
    for x in xrange(w):
        g[(x, y)] = closest((x, y), coords)


most_coord = None
most_area = -1
for p in coords:
    area = 0

    if not is_bound(p, coords):
        continue

    for q in g:
        if g[q] == p:
            area += 1

    print p, area

    if area > most_area:
        most_coord = p
        most_area = area


print "Solution 1:", most_area


region = []
thresh = 10000
for y in xrange(h):
    for x in xrange(w):
        dist = 0
        p = (x, y)
        for q in coords:
            dist += manhattan(p, q)
            if dist >= thresh:
                break

        if dist < thresh:
            region.append(p)

print "Solution 2:", len(region)
