#!/usr/bin/env python3
from sys import stdin
import re


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @property
    def length(self) -> int:
        return self.end - self.start

    def __repr__(self):
        return f"Range({self.start},{self.end})"

    def __contains__(self, value: int):
        return self.start <= value <= self.end

    def split(self, value: int, condition: str) -> tuple['Range', 'Range']:
        if not value in self:
            if value < self.start:
                return (None, Range(self.start, self.end))
            else:
                return (Range(self.start, self.end), None)

        if condition == "<":
            return (Range(self.start, value - 1) if value - 1 >= self.start else None, Range(value, self.end))
        else:
            return (Range(self.start, value), Range(value + 1, self.end) if value + 1 <= self.end else None)


class Rule:
    def __init__(self, category: str, condition: str, value: int):
        self.category = category
        self.condition = condition
        self.value = value

    def __repr__(self):
        return f"Rule({self.category} {self.condition} {self.value})"

    def apply(self, part: dict[str, Range]) -> tuple[Range, Range]:
        below, above = part[self.category].split(self.value, self.condition)
        if self.condition == "<":
            return (below, above)
        else:
            return (above, below)


def process_workflows(workflows, queue):
    accepted = []
    rejected = []
    while len(queue) > 0:
        part = queue.pop(0)

        wf = "in"
        while wf != "A" and wf != "R":
            for rule, destination in workflows[wf]:
                if rule is None:
                    wf = destination
                    break

                match_range, mismatch_range = rule.apply(part)

                if match_range is not None:
                    part[rule.category] = match_range
                    wf = destination

                    if mismatch_range is not None:
                        new_part = {k: v for k, v in part.items()}
                        new_part[rule.category] = mismatch_range
                        queue.append(new_part)
                    break

        if wf == "A":
            accepted.append(part)
        else:
            rejected.append(part)

    return accepted, rejected


indata = stdin.read().strip().split("\n\n")

workflows = {}
for line in indata[0].splitlines():
    name, rules = re.search(r"^([^\}]+)\{([^\}]+)\}$", line).groups()
    workflows[name] = []
    for rule in rules.split(","):
        if ":" in rule:
            cat, cond, value, dest = re.search(r"([^<>]+)([<>])(\d+):(.+)", rule).groups()
            r = Rule(cat, cond, int(value))
            workflows[name].append((r, dest))
        else:
            workflows[name].append((None, rule))

# Part 1
queue = []
for partline in indata[1].splitlines():
    part = {}
    for partvalue in partline[1:-1].split(","):
        name, value = partvalue.split("=")
        part[name] = Range(int(value), int(value))

    queue.append(part)

accepted, rejected = process_workflows(workflows, queue)
print(sum(sum(v.start for v in p.values()) for p in accepted))

# Part 2
part = {'x': Range(1, 4000), 'm': Range(1, 4000), 'a': Range(1, 4000), 's': Range(1, 4000)}
queue = [part]
accepted, rejected = process_workflows(workflows, queue)

combinations = 0
for part in accepted:
    t = (part['x'].length + 1) * (part['m'].length + 1) * (part['a'].length + 1) * (part['s'].length + 1)
    combinations += t
print(combinations)
