#!/usr/bin/env python3
import re
import sys

input_data = sys.stdin.read()

groups = input_data.strip().split("\n\n")

class SeedRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = end - start

    def overlaps(self, other):
        if self.start <= other.start and other.start < self.end:
            return True
        if self.start < other.end and other.end <= self.end:
            return True
        if other.start <= self.start and self.start < other.end:
            return True
        if other.start < self.end and self.end <= other.end:
            return True
        return False

    def split(self, other):
        if not self.overlaps(other):
            return [self]

        if self.start >= other.start and self.end <= other.end:
            return [self]

        if self.start < other.start and self.end <= other.end:
            a = SeedRange(self.start, other.start)
            b = SeedRange(other.start, self.end)
            return [a, b]

        elif self.start < other.start and self.end > other.end:
            a = SeedRange(self.start, other.start)
            b = SeedRange(other.start, other.end)
            c = SeedRange(other.end, self.end)
            return [a, b, c]

        elif self.start >= other.start and self.end > other.end:
            a = SeedRange(self.start, other.end)
            b = SeedRange(other.end, self.end)
            return [a, b]

        raise Exception("this should not happen")

seed_ranges = [SeedRange(int(x), int(x)+int(y)) for x, y in re.findall(r"(\d+)\s(\d+)", groups[0])]

for group in groups[1:]:
    lines = group.split("\n")[1:]

    queue = [sr for sr in seed_ranges]
    mapped = []

    while len(queue) > 0:
        seedrange = queue.pop(0)

        for line in lines:
            dst, src, length = (int(x) for x in re.findall("\d+", line))
            maprange = SeedRange(src, src+length)

            if not seedrange.overlaps(maprange):
                continue

            split_ranges = seedrange.split(maprange)

            for sr in split_ranges:
                pass


            break
        else:
            mapped.append(seedrange)

#print(min(seeds))
