#!/usr/bin/python
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

f = open('oscar.manas_pubkeyRSA_pseudo.pem','r')
buff = f.read()
f.close()

pkey = RSA.importKey(buff)
n = pkey.n
e = pkey.e
print 'n:', n
print 'e:', e

# sage: factor(n) -> 13819589958191161511^16 * 235063665088597395103381104073463970497^8
p = 13819589958191161511
q = 235063665088597395103381104073463970497
phi = (n*(p-1)*(q-1))/(p*q)

d = mulinv(e,phi)
print 'd:', d

privkey = RSA.construct((n,e,d))
f = open('oscar.manas_privkeyRSA_pseudo.pem','w')
f.write(privkey.exportKey())
f.close()

# openssl rsautl -decrypt -in oscar.manas_RSA_pseudo.enc -out oscar.manas_RSA_pseudo.dec -inkey oscar.manas_privkeyRSA_pseudo.pem