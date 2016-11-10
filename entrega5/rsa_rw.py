#!/usr/bin/python
import os
from fractions import gcd
from Crypto.PublicKey import RSA

# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def get_pkey(file):
	f = open(file,'r')
	buff = f.read()
	f.close()
	return RSA.importKey(buff)

pkey = get_pkey('oscar.manas_pubkeyRSA_RW.pem')
n = pkey.n
e = pkey.e
print 'n:', pkey.n
print 'e:', pkey.e

folder = 'keys/'
for file in os.listdir(folder):
	pkey2 = get_pkey(folder + file)
	n2 = pkey2.n
	p = gcd(n,n2)
	if p > 1:
		print file
		break

q = n / p
phi = (p-1)*(q-1)

d = mulinv(e,phi)
print 'd:', d

privkey = RSA.construct((n,e,d))
f = open('oscar.manas_privkeyRSA_RW.pem','w')
f.write(privkey.exportKey())
f.close()

# openssl rsautl -decrypt -in oscar.manas_RSA_RW.enc -out oscar.manas_RSA_RW.dec -inkey oscar.manas_privkeyRSA_RW.pem