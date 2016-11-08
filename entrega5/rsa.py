#!/usr/bin/python
from Crypto.PublicKey import RSA
from sympy.ntheory import factorint

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

f = open('oscar.manas_pubkeyRSA_pseudo.pem','r')
buff = f.read()
f.close()

pkey = RSA.importKey(buff)
n = pkey.n
e = pkey.e
print n
print e

#print factorint(n)
p = 13819589958191161511
q = 235063665088597395103381104073463970497
phi = (n*(p-1)*(q-1))/(p*q)

d = mulinv(e,phi)
print d

privkey = RSA.construct((n,e,d,p,q))
f = open('oscar.manas_privkeyRSA_pseudo.pem','w')
f.write(privkey.exportKey())
f.close()

# openssl rsautl -decrypt -in oscar.manas_RSA_pseudo.enc -out plaintext -inkey oscar.manas_privkeyRSA_pseudo.pem