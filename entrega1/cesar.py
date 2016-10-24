#!/usr/bin/python
from __future__ import print_function
import sys
import string
from collections import Counter
from utils import freqs

eng_freqs = ['E','T','A','O','N','R','I','S','H','D','L','F','C','M','U','G','Y','P','W','B','V','K','X','J','Q','Z']

f = open('2016_09_12_19_01_03_oscar.manas.Cesar', 'r')
cip = f.read()
f.close()

letters = filter(lambda c: c in string.ascii_letters, cip.upper())
cip_freqs = map(lambda x: chr(x+ord('A')),freqs(letters))
diffs = []
for k,v in zip(cip_freqs,eng_freqs):
	diffs.append((ord(k)-ord(v))%26)
k = Counter(diffs).most_common(1)[0][0]

print(k)

msg = []
for c in cip:
	if c in string.ascii_lowercase:
		msg.append(chr((ord(c)-ord('a')-k)%26+ord('a')))
	elif c in string.ascii_uppercase:
		msg.append(chr((ord(c)-ord('A')-k)%26+ord('A')))
	else:
		msg.append(c)

f = open('oscar.manas_14.cesar', 'w')
f.write(''.join(msg))
f.close()