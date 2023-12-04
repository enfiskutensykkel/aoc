#!/usr/bin/env python3
import re

test = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

expr = re.compile(r'(\d+)')

cards = {}

def add_card(card, instances):
    if card not in cards:
        cards[card] = instances
    else:
        cards[card] += instances


def play_card(card, winning, numbers):
    global cards

    add_card(card, 1)
    instances = cards[card]

    num_winning = 0
    for mynum in numbers:
        for winnum in winning:
            if winnum == mynum:
                num_winning += 1
                add_card((card + num_winning), instances)


#for line in test.strip().split("\n"):
for line in open("input.txt").readlines():
    card, winning, numbers = re.split(r"[:|]", line)
    card = int(expr.search(card).group(0))
    winning = sorted([int(i) for i in expr.findall(winning)])
    numbers = sorted([int(i) for i in expr.findall(numbers)])

    play_card(card, winning, numbers)

print(sum(cards.values()))
