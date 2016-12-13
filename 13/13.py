#!/usr/bin/env python

def is_wall(x, y, c):
    return len(filter(lambda x: x == '1', bin(x*x + 3*x + 2*x*y + y + y*y + c)[2:])) % 2 != 0


def find_neighbours(node, constant):
    x, y = node
    n = set()

    if y - 1 >= 0 and not is_wall(x, y - 1, constant):
        n.add((x, y-1))

    if not is_wall(x, y + 1, constant):
        n.add((x, y+1))

    if x - 1 >= 0 and not is_wall(x - 1, y, constant):
        n.add((x-1, y))

    if not is_wall(x + 1, y, constant):
        n.add((x+1, y))

    return n


def find_min(frontier):
    n, c = None, 10**6

    for node, cost in frontier:
        if cost < c:
            n = node
            c = cost

    return n, c


def contains(frontier, n, c=-1):
    for node, cost in frontier:
        if node == n:
            return cost > c
    return False


def replace(frontier, n, c):
    for node, cost in frontier:
        if node == n:
            frontier.remove((node, cost))
            break

    frontier.add((n, c))


def uniform_cost_search(start, goal, constant):
    node = start
    cost = 0

    frontier = set()
    frontier.add((node, cost))
    explored = set()

    while True:
        if len(frontier) == 0:
            return -1

        node, cost = find_min(frontier)
        frontier.remove((node, cost))

        if node == goal:
            return cost

        explored.add(node)

        for neighbour in find_neighbours(node, constant):
            if not neighbour in explored:
                if not contains(frontier, neighbour):
                    frontier.add((neighbour, cost+1))
                elif contains(frontier, neighbour, cost+1):
                    replace(frontier, neighbour, cost+1)

print uniform_cost_search((1,1), (31,39), 1352)
