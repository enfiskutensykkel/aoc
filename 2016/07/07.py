#!/usr/bin/env python
import re

def abba(string):
    for i in xrange(len(string)):
        if string[i:i+2] == string[i+3:i+1:-1]:
            return string[i] != string[i+1]

    return False

def ababab(aba, bab):
    for i in xrange(len(aba) - 2):
        if aba[i] == aba[i+2] and aba[i] != aba[i+1]:
            aba_part = aba[i:i+3]

            for j in xrange(len(bab) - 2):
                if bab[j] == aba_part[1] and bab[j+1] == aba_part[0] and bab[j+2] == aba_part[1]:
                    return aba_part, bab[j:j+3]

    return None

def tls(string):
    is_tls = False
    for match in re.finditer(r'(?=\[(?P<hyper>[^\]]+)\])|(?P<addr>[^\[]+)', string):
        hyper, addr = match.groups()

        if not hyper is None and abba(hyper):
            return False

        elif not addr is None and abba(addr):
            is_tls = True

    return is_tls

def ssl(string):
    nets = re.compile(r'\]?([^\[\]]+)\[?').findall(string)

    for supernet in nets[::2]:
        for hypernet in nets[1::2]:
            if ababab(supernet, hypernet):
                return True

    return False


num_tls = 0
num_ssl = 0

#print tls('abba[mnop]qrst')
#print tls('abcd[bddb]xyyx')
#print tls('aaaa[qwer]tyui')
#print tls('ioxxoj[asdfgh]zxcvbn')

#print ssl('aba[bab]xyz')
#print ssl('xyx[xyx]xyx')
#print ssl('aaa[kek]eke')
#print ssl('zazbz[bzb]cbd')
#
#print ssl('test[test]abc[bca]qwerty')
#print ssl('testaba[tst]bab[bab]aba[sts]aaa')

for line in open('input').readlines():
    num_tls += tls(line.strip())
    num_ssl += ssl(line.strip())

print "tls:", num_tls, "ssl:", num_ssl
