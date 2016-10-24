#!/usr/bin/python
from __future__ import print_function
import sys
import string

f = open('2016_09_12_19_01_03_oscar.manas.Escitalo', 'r')
cip = f.read()
f.close()

k = 7
print(k)

msg = []
for i in range(k):
	msg.append(cip[i::k])
msg.append('\n')

f = open('oscar.manas_7.escital', 'w')
f.write(''.join(msg))
f.close()