#!/usr/bin/python
from __future__ import print_function
import sys
import string
from collections import Counter
from utils import freqs

eng_freqs = ['E','T','A','O','N','R','I','S','H','D','L','F','C','M','U','G','Y','P','W','B','V','K','X','J','Q','Z']

f = open('2016_09_12_19_01_03_oscar.manas.Vigenere', 'r')
cip = f.read()
f.close()

n = int(sys.argv[1])
letters = filter(lambda c: c in string.ascii_letters, cip.upper())
shifts = []
for i in range(n):
	cip_freqs = map(lambda x: chr(x+ord('A')),freqs(letters[i::n]))
	diffs = []
	for k,v in zip(cip_freqs,eng_freqs):
		diffs.append((ord(k)-ord(v))%26)
	s = Counter(diffs).most_common(1)[0][0]
	shifts.append(s)

print(map(lambda c: chr(c+ord('A')),shifts))

i = 0
msg = []
for c in cip:
	k = shifts[i]
	if c in string.ascii_letters:	
		if c in string.ascii_lowercase:
			msg.append(chr((ord(c)-ord('a')-k)%26+ord('a')))
		elif c in string.ascii_uppercase:
			msg.append(chr((ord(c)-ord('A')-k)%26+ord('A')))
		i = (i+1)%len(shifts)
	else:
		msg.append(c)

f = open('oscar.manas_home.vigenere', 'w')
f.write(''.join(msg))
f.close()