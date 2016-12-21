#!/usr/bin/env sage
import urllib2
import OpenSSL
import subprocess
from build_hash import digest

## Exercise 1 #################################################################
print '## Exercise 1 #########################################'

# Curve P-256 (from http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
print 'Curve P-256'
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E = EllipticCurve(Zmod(p),[a,b])
assert(E.cardinality()==n)

# Check that cardinality of the curve is prime
print 'Prime order?', is_prime(E.cardinality())

# Point P (subjectPublicKey)
pubkey = '04e6ecdcce7e73e8344f1ae129f66de1d463c65fcda70e91e36a41f66430fb01ec98a2b9fe63ef07ec0950990e91f9ca5616db1c10e85184c7b062055209fcce1c'
Px = Integer(pubkey[2:2+64],16)
Py = Integer(pubkey[-64:],16)
P = E([Px,Py])

# Check if P belongs to E
print 'Generator point P belongs to the curve?', P in E

# Order of P
print 'Order of point P:', P.order()

# Check signature
signature = '3046022100b3363e0acb7ef124de271e5d14c0270a0694d277815993e65997156eeb058d64022100f5261d8d5b02ea67af0ef5b7bd184c992a0a36738da3846a17188704cedbf323'
f1 = Integer(signature[8:8+66],16)
f2 = Integer(signature[-66:],16)
h = digest()

G = E([Gx,Gy])
q = G.order()
assert(q==n)

w = mod(f2**(-1),q)
w1 = mod(h*w,q);
w2 = mod(f1*w,q);
v = Integer(w1)*G+Integer(w2)*P
print 'Correct signature?', mod(v[0],q) == f1


## Exercise 2 #################################################################
print '\n## Exercise 2 #########################################'

print 'Website: twitter.com'

# Curve P-256 (from http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
print 'Curve P-256'
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E = EllipticCurve(Zmod(p),[a,b])

pubkey = '04529368ee3a246ce3f7e0cf5c4df851aeccb47ee452fd2a37c71824da6469d528673065f07c82d79bacaf8dca27835c21ea8eae8c085a3ebc42af995524f132aa'
Px = int(pubkey[2:2+64],16)
Py = int(pubkey[-64:],16)
P = E([Px,Py])
assert(P in E)

G = E([Gx,Gy])
dni = 77620769

# privkey resulting from concatenating my dni 8 times, and the associated pubkey
privkey = int(str(dni)*8)
pubkey = privkey * G
print 'pubkey:', pubkey

# pubkey that has my dni as component x of the point
x = dni
z = mod(x**3+a*x+b,p)
assert(mod(z**((p-1)/2),p)==1) # check that z is a square
y = mod(z**((p+1)/4),p) # compute the square root of z, which is the y component of the point
Q = E([x,y])
assert(Q in E)
print 'Q:', Q

# We can't find the privkey associated to the pubkey Q because it's the Discrete
# Logarithm Problem, which is conjetured intractable.
# print discrete_log(Q, G, G.order(), operation='+') # takes forever

# Even trying to generate the pubkey from a known privkey, I haven't been able
# to find a pubkey that starts with my dni in a reasonable time.
# for r in range(G.order()): if str(r*G).startswith(str(dni)): print r*G; break # takes forever


## Exercise 3 #################################################################
print '\n## Exercise 3 #########################################'

CRL_URI = 'http://sr.symcb.com/sr.crl'
crl_file = urllib2.urlopen(CRL_URI)
crl_object = OpenSSL.crypto.load_crl(OpenSSL.crypto.FILETYPE_ASN1, crl_file.read())
crl_file.close()
revoked_objects = crl_object.get_revoked()
print 'CRL revoked certificates:', len(revoked_objects)

# curl http://sr.symcb.com/sr.crt > sr.crt
# openssl x509 -in sr.crt -inform der -out sr.pem
# cat SymantecClass3EVSSLCA-G3.crt VeriSignClass3PublicPrimaryCertificationAuthority-G5.crt > chain.crt
# openssl ocsp -issuer chain.crt -cert twitter.crt -url http://sr.symcd.com -CAfile sr.pem
try:
	subprocess.check_output(['openssl','ocsp','-issuer','chain.crt','-cert','twitter.crt','-url','http://sr.symcd.com','-CAfile','sr.pem'])
except subprocess.CalledProcessError as e:
	print e.output