#!/usr/bin/env python3
import re

total_points = 0

games = open("input.txt").readlines()
cards = [1] * len(games)

for card, line in enumerate(games):
    numbers = re.findall(r'\d+', line)[1:]
    winning = len(numbers) - len(set(numbers))
    total_points += (2 ** (winning - 1)) if winning > 0 else 0

    for next_card in range(card+1, card+1+winning):
        cards[next_card] += cards[card]

print(total_points)
print(sum(cards))
