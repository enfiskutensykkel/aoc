#!/usr/bin/env python
from hashlib import md5
from sys import exit

def hash(salt, index):
    h = md5(salt + str(index)).hexdigest()

    k = 0
    while k < 2016:
        h = md5(h).hexdigest()
        k += 1

    return h

def successive(s, n):
    for i in xrange(len(s) - (n-1)):
        ss = s[i:i+n]

        if len(filter(lambda x: x == ss[0], ss)) == n:
            return ss[0]

    return None


def generate(hashes, salt, start, end):
    print "generating hashes..."
    for i in xrange(start, end):
        h = hash(salt, i)
        s = successive(h, 5)

        if not s is None:
            hashes[i] = s

#salt = 'abc'
salt = 'jlmsuwbz'
hashes = {}

index = 0
keys = 0
generated = 0


while keys < 64:

    while index + 1000 > generated:
        generate(hashes, salt, generated, generated + 1000)
        generated += 1000

    h = hash(salt, index)

    s = successive(h, 3)

    if not s is None:
        for k in xrange(index + 1, index + 1001):
            if hashes.has_key(k) and hashes[k] == s:
                keys += 1
                print "key #%d found, index=%d (k=%d)" % (keys, index, k)
                break

    index += 1

print index - 1
