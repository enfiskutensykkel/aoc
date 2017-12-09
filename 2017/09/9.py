#!/usr/bin/env python

#data = [
#        "{}",
#        "{{{}}}",
#        "{{},{}}",
#        "{{{},{},{{}}}}",
#        "{<a>,<a>,<a>,<a>}",
#        "{{<ab>},{<ab>},{<ab>},{<ab>}}",
#        "{{<!!>},{<!!>},{<!!>},{<!!>}}",
#        "{{<a!>},{<a!>},{<a!>},{<ab>}}"
#        ]

data = [
        "<>",
        "<random characters>",
        "<<<<>",
        "<{!>}>",
        "<!!>",
        "<!!!>>",
        "<{o\"i!a,<{i<a>"
        ]


def score(s):
    escape = False
    garbage = False
    groups = 0
    score = 0
    gc = 0

    for c in s:
        if not escape and c == "!":
            escape = True

        elif not escape and not garbage:
            if c == "{":
                groups += 1
                score += groups
            elif c == "}":
                groups -= 1
            elif c == "<":
                garbage = True

        elif not escape and garbage:
            if c == ">":
                garbage = False
            else:
                gc += 1

        elif escape:
            escape = False

    return score, gc

print score(open('input').read())
