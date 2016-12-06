#!/usr/bin/env python

message = []

for line in open('input').readlines():
    for i, c in enumerate(line.strip()):
        if i == len(message):
            message.append({})

        if not message[i].has_key(c):
            message[i][c] = 0

        message[i][c] += 1

corrected = ""
for chardict in message:
    #corrected += max(chardict.items(), key=lambda x: x[1])[0]
    corrected += min(chardict.items(), key=lambda x: x[1])[0]


print corrected

