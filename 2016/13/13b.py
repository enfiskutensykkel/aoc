#!/usr/bin/env python

def is_wall(x, y, c):
    return len(filter(lambda x: x == '1', bin(x*x + 3*x + 2*x*y + y + y*y + c)[2:])) % 2 != 0


def find_min(queue, dist):
    node = None
    cost = 10**6

    for u in queue:
        if dist[u] <= cost:
            cost = dist[u]
            node = u

    return node


def find_neighbours(u, steps, puzzle):
    x, y = u
    n = set()

    if y - 1 >= 0 and not is_wall(x, y-1, puzzle):
        n.add((x, y-1))

    if y + 1 < steps and not is_wall(x, y+1, puzzle):
        n.add((x, y+1))

    if x - 1 >= 0 and not is_wall(x-1, y, puzzle):
        n.add((x-1, y))

    if x + 1 < steps and not is_wall(x+1, y, puzzle):
        n.add((x+1, y))

    return n


def dijkstra(src, steps, puzzle):
    q = set()
    dist = {}

    for y in xrange(steps*2):
        for x in xrange(steps*2):
            v = (x, y)
            dist[v] = 10**6
            q.add(v)

    dist[src] = 0

    while len(q) > 0:
        u = find_min(q, dist)
        q.remove(u)

        for v in find_neighbours(u, steps*2, puzzle):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt

    return dist

dist = dijkstra((1,1), 50, 1352)
#dist = dijkstra((1,1), 10, 10)
count = 0

for cost in dist.itervalues():
    if cost <= 50:
        count += 1

print count
