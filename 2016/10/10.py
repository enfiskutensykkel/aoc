#!/usr/bin/env python
import re

class Bin(object):
    bins = {}

    def __init__(self):
        self.values = []

    def recv_value(self, value):
        self.values.append(value)

    @classmethod
    def get_bin(cls, name):
        if not name in cls.bins:
            cls.bins[name] = Bin()
        return cls.bins[name]


class Bot(object):
    bots = {}

    def __init__(self, name):
        self.name = name
        self.low = None
        self.high = None

    def can_act(self):
        return self.low != None and self.high != None

    def recv_value(self, value):
        if self.low == None:
            self.low = value
            return

        self.high = value
        if value < self.low:
            self.high = self.low
            self.low = value

        if self.low == 17 and self.high == 61:
            print "bot %d handles 17 and 61" % (self.name)

    @classmethod
    def get_bot(cls, name):
        if not name in cls.bots:
            cls.bots[name] = Bot(name)
        return cls.bots[name]


#lines = [
#        'value 5 goes to bot 2',
#        'bot 2 gives low to bot 1 and high to bot 0',
#        'value 3 goes to bot 1',
#        'bot 1 gives low to output 1 and high to bot 0',
#        'bot 0 gives low to output 2 and high to output 0',
#        'value 2 goes to bot 2'
#        ]
orders = []

#for line in lines:
for line in open('input').readlines():
    m1 = re.match(r'value (\d+) goes to bot (\d+)', line.strip())
    m2 = re.match(r'bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)', line.strip())

    if m1:
        bot = int(m1.group(2))
        value = int(m1.group(1))
        Bot.get_bot(bot).recv_value(value)

    elif m2:
        bot = int(m2.group(1))
        lo_recv_name = int(m2.group(3))
        hi_recv_name = int(m2.group(5))

        lo_recv = Bin.get_bin(lo_recv_name) if m2.group(2) == 'output' else Bot.get_bot(lo_recv_name)
        hi_recv = Bin.get_bin(hi_recv_name) if m2.group(4) == 'output' else Bot.get_bot(hi_recv_name)

        orders.append((Bot.get_bot(bot), lo_recv, hi_recv))

while len(orders) > 0:
    new_orders = []

    for bot, lo, hi in orders:
        if bot.can_act():
            lo.recv_value(bot.low)
            hi.recv_value(bot.high)
            bot.low = bot.high = None
        else:
            new_orders.append((bot, lo, hi))

    orders = new_orders

print Bin.get_bin(0).values[0] * Bin.get_bin(1).values[0] * Bin.get_bin(2).values[0]
