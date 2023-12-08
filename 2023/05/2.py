#!/usr/bin/env python3
import re
import sys
import bisect

input_data = sys.stdin.read()

groups = input_data.strip().split("\n\n")

class SeedRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def length(self):
        return self.end - self.start

    def overlaps(self, other):
        return (self.start <= other.start < self.end) or (other.start <= self.start < other.end)

    def __lt__(self, other):
        return self.start < other.start or self.end < other.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def split(self, other):
        if self.start >= other.start and self.end <= other.end:
            a = SeedRange(self.start, self.end)
            return (None, a, None)

        elif self.start >= other.start and self.end > other.end:
            a = SeedRange(self.start, other.end)
            b = SeedRange(other.end, self.end)
            return (None, a, b)

        elif self.start < other.start and self.end <= other.end:
            a = SeedRange(self.start, other.start)
            b = SeedRange(other.start, self.end)
            return (a, b, None)

        elif self.start < other.start and self.end > other.end:
            a = SeedRange(self.start, other.start)
            b = SeedRange(other.start, other.end)
            c = SeedRange(other.end, self.end)
            return (a, b, c)

        raise Exception("this should not happen")


seed_ranges = sorted([SeedRange(int(x), int(x)+int(y)) for x, y in re.findall(r"(\d+)\s(\d+)", groups[0])])

for group in groups[1:]:
    lines = group.split("\n")[1:]
    print(group.split("\n")[0].split()[0])
    mapped = []

    mappings = [tuple(int(x) for x in re.findall("\d+", line))
                for line in lines]
    mapping_objs = sorted([(dst, SeedRange(src, src+length))
                          for dst, src, length in mappings],
                          key=lambda x: x[1])

    last = mapping_objs[-1][1]

    while len(seed_ranges) > 0:
        seedrange = seed_ranges.pop(0)

        if seedrange.start >= last.end:
            bisect.insort_left(mapped, seedrange)
            continue

        for dst, maprange in mapping_objs:
            if seedrange.end <= maprange.start:
                bisect.insort_left(mapped, seedrange)
                break

            if not seedrange.overlaps(maprange):
                continue

            before, overlapping, after = seedrange.split(maprange)

            if before:
                bisect.insort_left(seed_ranges, before)

            if overlapping:
                offset = overlapping.start - maprange.start
                bisect.insort_left(mapped, SeedRange(dst + offset, dst + offset + overlapping.length))

            if after:
                bisect.insort_left(seed_ranges, after)

            break
        else:
            bisect.insort_left(mapped, seedrange)

    seed_ranges.append(mapped[0])

    # merge ranges
    for idx in range(1, len(mapped)):
        next_range = mapped[idx]
        prev_range = seed_ranges[-1]

        if prev_range.end < next_range.start:
            seed_ranges.append(next_range)

        elif prev_range.end >= next_range.start and next_range.end > prev_range.end:
            prev_range.end = next_range.end

print(seed_ranges[0].start)
