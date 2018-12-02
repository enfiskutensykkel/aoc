#!/usr/bin/env python

def letter_counts(s):
    counts = {}
    for c in s:
        counts[c] = 0
        for d in s:
            if c == d:
                counts[c] += 1

    return [(char, count) for char, count in counts.iteritems() if count > 1]

def twos_or_threes(letter_counts):
	has_two = False
	has_three = False
	for char, count in letter_counts:
		if count == 2:
			has_two = True
		elif count == 3:
			has_three = True

	return has_two, has_three

data = [line.strip() for line in open('input').readlines()]
#data = ["abcdef", "bababc", "abbcde", "abccd", "aabcdd", "abcdee", "ababab"]

twos = 0
threes = 0

for line in data:
    counts = letter_counts(line)
    two, three = twos_or_threes(counts)
    twos += two
    threes += three

print twos * threes
