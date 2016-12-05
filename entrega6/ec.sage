#!/usr/bin/env sage

## Exercise 1 #################################################################
print '## Exercise 1 ###################################'

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
pubkey = '04794950e23cb2ae663676db17d86c0a628e4776b71084baca3e9104dfc377ad54c9c6406e5f89f9e40462588e360ba9f068a62b95d93726408a720c5f0b2bdd21'
Px = int(pubkey[2:66],16)
Py = int(pubkey[66:],16)
P = E(Px,Py)

# Check if P belongs to E
print 'Generator point P belongs to the curve?', mod(Py**2,p)==mod(Px**3+a*Px+b,p)

# Order of P
print 'Order of point P:', P.order()

# Check certificate
signature = '3046022100b3363e0acb7ef124de271e5d14c0270a0694d277815993e65997156eeb058d64022100f5261d8d5b02ea67af0ef5b7bd184c992a0a36738da3846a17188704cedbf323'
f1 = Integer(signature[8:8+66],16)
f2 = Integer(signature[-66:],16)
print 'f1:', signature[8:8+66]
print 'f2:', signature[-66:]
#f8ce0926c6631c729b9f37d5f9725f2c60dca677993f815fb810244bd9371681527baf231fec3b2c72fbfa663116ec6fc6366fcad958b884db63919a9344a19f
h = 0xf8ce0926c6631c729b9f37d5f9725f2c60dca677993f815fb810244bd9371681
G = E(Gx,Gy)
q = G.order()
assert(q == E.cardinality())

w = mod(f2**(-1),q)
w1 = mod(h*w,q);
w2 = mod(f1*w,q);
v = Integer(w1)*G+Integer(w2)*P
print 'Correct signature?', mod(v[0],q) == f1


## Exercise 2 #################################################################
print '\n## Exercise 2 ###################################'

# Web site: twitter.com

# Curve P-256 (from http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
print 'Curve P-256'
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E = EllipticCurve(Zmod(p),[a,b])

pubkey = '04529368ee3a246ce3f7e0cf5c4df851aeccb47ee452fd2a37c71824da6469d528673065f07c82d79bacaf8dca27835c21ea8eae8c085a3ebc42af995524f132aa'
Px = int(pubkey[2:66],16)
Py = int(pubkey[66:],16)
P = E(Px,Py)
assert(mod(Py**2,p)==mod(Px**3+a*Px+b,p))

G = E(Gx,Gy)
dni = 77620769

privkey = int(str(dni)*8)
pubkey = privkey * G
print 'pubkey:', pubkey

x = dni
z = mod(x**3+a*x+b,p)
assert(mod(z**((p-1)/2),p)==1)
y = z**((p+1)/4)
Q = E(x,y)
assert(mod(y**2,p)==mod(x**3+a*x+b,p))
print 'Q:', Q

# We can't find the private key associated to the public key Q because 
# it's the Discrete Logarithm Problem, which is conjetured intractable
# print discrete_log(Q,G,G.order(),operation='+') # takes forever

