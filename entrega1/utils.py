#!/usr/bin/python
import sys
import string

def freqs(msg):
	freqs = [0] * 26
	for c in msg:
		if c in string.ascii_lowercase:
			freqs[ord(c)-ord('a')] += 1
		elif c in string.ascii_uppercase:
			freqs[ord(c)-ord('A')] += 1
	freqs = dict(zip(range(26),freqs))
	return map(lambda x: x[0], sorted(freqs.items(), key=lambda x: x[1]))[::-1]