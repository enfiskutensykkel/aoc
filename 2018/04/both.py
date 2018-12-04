#!/usr/bin/env python

import re

tsexpr = re.compile(r'^\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<min>\d{2})\]')
shiftexpr = re.compile(r'Guard #(\d+) begins shift')

#events = """[1518-11-01 00:00] Guard #10 begins shift
#[1518-11-01 00:05] falls asleep
#[1518-11-01 00:25] wakes up
#[1518-11-01 00:30] falls asleep
#[1518-11-01 00:55] wakes up
#[1518-11-01 23:58] Guard #99 begins shift
#[1518-11-02 00:40] falls asleep
#[1518-11-02 00:50] wakes up
#[1518-11-03 00:05] Guard #10 begins shift
#[1518-11-03 00:24] falls asleep
#[1518-11-03 00:29] wakes up
#[1518-11-04 00:02] Guard #99 begins shift
#[1518-11-04 00:36] falls asleep
#[1518-11-04 00:46] wakes up
#[1518-11-05 00:03] Guard #99 begins shift
#[1518-11-05 00:45] falls asleep
#[1518-11-05 00:55] wakes up"""
#events = sorted(events.split('\n'))

events = sorted([line.strip() for line in open('input').readlines()])

guards = {}

guard = None
prev = None
awake = False

for event in events:
    begin = shiftexpr.search(event)

    if begin:
        guard = int(begin.group(1))
        if not guard in guards:
            guards[guard] = [0 for i in range(60)]

        prev = 0
        awake = True

    else:
        match = tsexpr.match(event)

        if awake:
            prev = int(match.group('min'))
            awake = False
        else:
            awake = True
            curr = int(match.group('min'))

            for i in range(prev, curr):
                guards[guard][i] += 1

most = None
for guard in guards:
    if most is None or sum(guards[guard]) > sum(guards[most]):
        most = guard

n = -1
for i, k in enumerate(guards[most]):
    if n == -1 or k > guards[most][n]:
        n = i

freq = None
c = -1
for i in range(60):
    for guard in guards:
        if c == -1 or guards[guard][i] > guards[freq][c]:
            c = i
            freq = guard

print most, n, most * n
print freq, c, freq * c
