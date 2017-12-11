#!/usr/bin/env python

reverse = {
        'n': 's',
        'nw': 'se',
        'sw': 'ne',
        's': 'n',
        'se': 'nw',
        'ne': 'sw'
        }

neighbourhood = {
        'n': {'sw': 'nw', 'se': 'ne'},
        'nw': {'ne': 'n', 's': 'sw'},
        'sw': {'n': 'nw', 'se': 's'},
        's': {'nw': 'sw', 'ne': 'se'},
        'se': {'se': 's', 'n': 'ne'},
        'ne': {'s': 'se', 'nw': 'n'}
        }

neighbourhood_rlut = {
        'n': {'sw': 'se', 'se': 'sw'},
        'nw': {'ne': 's', 's': 'ne'},
        'sw': {'n': 'se', 'se': 'n'},
        's': {'nw': 'ne', 'ne': 'nw'},
        'se': {'se': 'n', 'n': 'se'},
        'ne': {'s': 'nw', 'nw': 's'}
        }


class Hexagon(object):
    def __init__(self, grid):
        self.adjacent = {}
        self.grid = grid
        grid.append(self)


    def create_neighbour(self, neighbour):
        adjacent = Hexagon(self.grid)
        self.adjacent[neighbour] = adjacent
        adjacent.adjacent[reverse[neighbour]] = self


    def populate_neighbourhood(self):
        for neighbour in neighbourhood.keys():
            if not neighbour in self.adjacent:
                self.create_neighbour(neighbour)

        for neighbour, neighbours in neighbourhood.items():
            for your_neighbour, my_neighbour in neighbours.items():
                self.adjacent[neighbour].adjacent[your_neighbour] = self.adjacent[my_neighbour]
                self.adjacent[my_neighbour].adjacent[reverse[your_neighbour]] = self.adjacent[neighbour]

        for neighbour, backwards in neighbourhood_rlut.items():
            for yy_neighbour, y_neighbour in backwards.items():
                self.adjacent[neighbour].adjacent[yy_neighbour].adjacent[y_neighbour] = self

    def get(self, neighbour):
        if not neighbour in self.adjacent:
            self.populate_neighbourhood()

        return self.adjacent[neighbour]



def find_min(q, dist):
    u = None
    for n in q:
        if u == None or dist[n] < dist[u]:
            u = n

    return u


# Do the Dijkstra
def distance(graph, source, target):
    dist = {}
    prev = {}
    q = []

    for v in graph:
        dist[v] = 10**7
        prev[v] = None
        q.append(v)

    dist[source] = 0

    while len(q) > 0:
        u = find_min(q, dist)
        if u == target:
            break

        q.remove(u)

        for v in u.adjacent.values():
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist[target]


#tests = ["ne,ne,ne", "ne,ne,sw,sw", "ne,ne,s,s", "se,sw,se,sw,sw"]
#path = tests[3].split(',')

path = open('input').read().strip().split(',')

graph = []
hexagon = start = Hexagon(graph)
for step in path:
    hexagon = hexagon.get(step)

print distance(graph, hexagon, start)
print distance(graph, start, hexagon)

