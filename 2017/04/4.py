#!/usr/bin/env python


valid = 0
not_anagrams = 0
neither = 0

for phrase in open('input').readlines():
    unique = set()
    sunique = set()
    invalid = False
    anagram = False

    for word in phrase.strip().split():
        if word in unique:
            invalid = True

        sword = "".join(sorted(word))
        if sword in sunique:
            anagram = True

        unique.add(word)
        sunique.add(sword)

    if not invalid:
        valid += 1

    if not anagram:
        not_anagrams += 1

    if not anagram and not invalid:
        neither += 1

print valid
print not_anagrams
print neither
