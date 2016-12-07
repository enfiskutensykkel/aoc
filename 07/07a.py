#!/usr/bin/env python
import re

def abba(string):
    for i in xrange(len(string)):
        if string[i:i+2] == string[i+3:i+1:-1]:
            return string[i] != string[i+1]

    return False

def tls(string):
    is_tls = False
    for match in re.finditer(r'(?=\[(?P<hyper>[^\]]+)\])|(?P<addr>[^\[]+)', string):
        hyper, addr = match.groups()

        if not hyper is None and abba(hyper):
            return False

        elif not addr is None and abba(addr):
            is_tls = True

    return is_tls


num_ips = 0

print tls('abba[mnop]qrst')
print tls('abcd[bddb]xyyx')
print tls('aaaa[qwer]tyui')
print tls('ioxxoj[asdfgh]zxcvbn')

for line in open('input').readlines():
    num_ips += tls(line.strip())

print num_ips
