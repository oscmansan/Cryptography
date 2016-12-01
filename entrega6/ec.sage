#!/usr/bin/env sage

# Curve P-256 (from http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
print 'Curve P-256'
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E = EllipticCurve(Zmod(p),[a,b])

# Check that cardinality of the curve is2 prime
print 'Prime order?', is_prime(E.cardinality())

# Point P
pubkey = '794950e23cb2ae663676db17d86c0a628e4776b71084baca3e9104dfc377ad54c9c6406e5f89f9e40462588e360ba9f068a62b95d93726408a720c5f0b2bdd21'
Px = int(pubkey[:64],16)
Py = int(pubkey[64:],16)
P = E(Px,Py)

# Check if P belongs to E
print 'Generator point P belongs to the curve?', mod(Py**2,p)-mod(Px**3+a*Px+b,p)==0

# Order of P
print 'Order of point P:', P.order()

#Check certificate
signature = '3046022100b3363e0acb7ef124de271e5d14c0270a0694d277815993e65997156eeb058d64022100f5261d8d5b02ea67af0ef5b7bd184c992a0a36738da3846a17188704cedbf323'
f1 = int(signature[8:8+66],16)
f2 = int(signature[-66:],16)
print len(signature)
print 'f1', signature[8:8+66]
print 'f2', signature[-66:]
hash_m = 0x1b71729becf5696ecf188ae0a6d83e559d2929a2
G = E(Gx,Gy)
q = G.order()

w = inverse_mod(f2,q)
w1 = (hash_m * w) % q;
w2 = (f1 * w) % q;
v = w1*G+w2*P
x = int(v[0])
print 'Correct certificate?', (x % q) == f1