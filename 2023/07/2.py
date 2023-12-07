#!/usr/bin/env python3
from sys import stdin


hands = [tuple(line.split())
         for line in stdin.read().strip().split("\n")]

def score_hand(hand):
    order = "J23456789TQKA"
    score = 1
    for i in range(5):
        score *= len(order)
        score += order.index(hand[i])
    return score


def permutations(cset, n):
    if n == 0:
        return []
    if n == 1:
        return list(cset)

    perms = permutations(cset, n-1)
    new_perms = []
    for p in perms:
        for c in cset:
            new_perms.append(p + c)

    return new_perms


def rank_hand(hand):
    copy = ""
    jokers = 0
    cset = set()
    for c in hand:
        if c == "J":
            jokers += 1
        else:
            cset.add(c)
            copy += c

    if jokers == 5:
        return 13

    offset = {5: 13,
              4: 11,
              3: 5,
              2: 2}

    if jokers > 0:
        variants = [sorted(copy + v) for v in permutations(cset, jokers)]
    else:
        variants = [sorted(hand)]

    mscore = 0
    for v in variants:

        i = 0
        score = 0
        while i < 5:
            j = i + 1
            while j < 5 and v[j] == v[i]:
                j += 1
            if j != i + 1:
                streak = j - i
                score += offset[streak]
            i = j

        mscore = max(mscore, score)

    return mscore


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
