#!/usr/bin/env python
import re


class Marble(object):
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def insert_after(self, new):
        new.next = self.next
        new.prev = self
        self.next.prev = new
        self.next = new
        return new

    def remove(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        self.next = self
        self.prev = self
        return self

    def walk_counter_clockwise(self, n):
        ptr = self
        while n > 0:
            ptr = ptr.prev
            n -= 1
        return ptr

def insert(current, number):
    marble = Marble(number)
    current.next.insert_after(marble)
    return marble



players, last = [int(i) for i in re.findall(r'\d+', open('input').read())]


def game(players, last):
    scores = dict((i, 0) for i in range(players))
    marbles = Marble(0)

    player = 0
    current = marbles
    next_number = 1

    while current.value != last:
        if next_number % 23 == 0:
            scores[player] += next_number
            other = current.walk_counter_clockwise(7)
            scores[player] += other.value
            current = other.next
            other.remove()
        else:
            current = insert(current, next_number)

        next_number += 1
        player = (player + 1) % len(scores)

    return max(scores.values())

print game(players, last)
print game(players, last*100)
