#!/usr/bin/env python3
from sys import stdin


hands = [tuple(line.split())
         for line in stdin.read().strip().split("\n")]

def score_hand(hand):
    order = "23456789TJQKA"
    score = 1
    for i in range(5):
        score *= len(order)
        score += order.index(hand[i])
    return score


def rank_hand(hand):
    copy = sorted(hand)

    offset = {5: 13,
              4: 11,
              3: 5,
              2: 2}

    i = 0
    score = 0
    while i < 5:
        j = i + 1
        while j < 5 and copy[j] == copy[i]:
            j += 1
        if j != i + 1:
            streak = j - i
            score += offset[streak] #+ order.index(hand[i])
        i = j

    return score

ranks = {}
for hand, bid in hands:
    rank = rank_hand(hand)
    if rank not in ranks:
        ranks[rank] = [(hand, int(bid))]
    else:
        ranks[rank].append((hand, int(bid)))

rank_keys = sorted(ranks.keys())

factor = 1
total = 0
for rank in rank_keys:
    ranks[rank].sort(key=lambda x: score_hand(x[0]))
    for hand, bid in ranks[rank]:
        total += bid * factor
        factor += 1
print(total)
