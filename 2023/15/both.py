#!/usr/bin/env python3
from sys import stdin

def hashcode(s):
    current_value = 0

    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value


def focusing_power(boxes, box):
    power = 0
    for i, fc in enumerate(boxes[box][1]):
        power += (box+1) * (i+1) * fc
    return power

sequences = stdin.read().strip().split(",")

print(sum(hashcode(seq) for seq in sequences))


boxes = []
for i in range(256):
    boxes.append(([], []))


for i, sequence in enumerate(sequences):
    key = None
    focal_length = None
    if sequence[-1] == "-":
        key = sequence[:-1]
    else:
        key, focal_length = sequence.split("=", 1)

    box = boxes[hashcode(key)]
    idx = len(box[0])
    try:
        idx = box[0].index(key)
    except ValueError:
        pass

    if focal_length is None:
        if idx != len(box[0]):
            box[0].pop(idx)
            box[1].pop(idx)

    else:
        if idx != len(box[0]):
            box[1][idx] = int(focal_length)
        else:
            box[0].insert(idx, key)
            box[1].insert(idx, int(focal_length))


total = 0
for i, box in enumerate(boxes):
    if len(box[0]) > 0:
        total += focusing_power(boxes, i)
print(total)
