#!/usr/bin/env python

#data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()
data = open('input').read().split()

class node(object):
    def __init__(self):
        self.children = []
        self.entries = []

    def sum_metadata(self):
        s = sum(self.entries)

        for child in self.children:
            s += child.sum_metadata()

        return s

    def find_value(self):
        if len(self.children) == 0:
            return sum(self.entries)

        value = 0
        for entry in self.entries:
            i = entry - 1
            if i < len(self.children):
                value += self.children[i].find_value()

        return value


def parse_node(data, pos):
    nchildren = int(data[pos])
    nentries = int(data[pos + 1])

    root = node()

    pos += 2
    while len(root.children) < nchildren:
        pos, child = parse_node(data, pos)
        root.children.append(child)

    while len(root.entries) < nentries:
        root.entries.append(int(data[pos]))
        pos += 1

    return pos, root


_, root = parse_node(data, 0)


print root.sum_metadata()
print root.find_value()
