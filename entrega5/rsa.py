#!/usr/bin/python
from OpenSSL import crypto
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

pkey = crypto.load_publickey(crypto.FILETYPE_PEM,buff)
RSAPublicKey = pkey.to_cryptography_key()
RSAPublicNumbers = RSAPublicKey.public_numbers()
n = RSAPublicNumbers.n
e = RSAPublicNumbers.e

print n
print e

#print factorint(n)

p = 13819589958191161511
q = 235063665088597395103381104073463970497
phi = (p-1)*(q-1)

d = mulinv(e,phi)
print d