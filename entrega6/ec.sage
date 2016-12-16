#!/usr/bin/env sage
import urllib2
import OpenSSL
import subprocess

## Exercise 1 #################################################################
print '## Exercise 1 ###################################'

# Curve P-256 (from http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
print 'Curve P-256'
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E = EllipticCurve(Zmod(p),[a,b])
print E
assert(E.cardinality()==n)

# Check that cardinality of the curve is prime
print 'Prime order?', is_prime(E.cardinality())

# Point P
pubkey = '04957da92c1cc4c61d749de0ecb13b5dd40fd200e34c317081141907d2ec122f804e5a0f178770bc231a0c01ea275afa3b3a7c3524c036f30ee03124929dc21ac1'
Px = Integer(pubkey[2:2+64],16)
Py = Integer(pubkey[-64:],16)
Px = 0x957da92c1cc4c61d749de0ecb13b5dd40fd200e34c317081141907d2ec122f80
Py = 0x4e5a0f178770bc231a0c01ea275afa3b3a7c3524c036f30ee03124929dc21ac1
P = E([Px,Py])

# Check if P belongs to E
print 'Generator point P belongs to the curve?', mod(Py**2,p)==mod(Px**3+a*Px+b,p)

# Order of P
print 'Order of point P:', P.order()

# Check certificate
signature = '304502205ccb3b85bcb3c500899004c1c70a266d9f88c4f2410e5e6a842be5fb759ffdd4022100ee779d07baf61c547a966778a3e2689165a91b8f3272ca9082bf23229737d74c'
f1 = Integer(signature[8:8+64],16)
f2 = Integer(signature[-66:],16)
f1 = 0x5ccb3b85bcb3c500899004c1c70a266d9f88c4f2410e5e6a842be5fb759ffdd4
f2 = 0x00ee779d07baf61c547a966778a3e2689165a91b8f3272ca9082bf23229737d74c
# m = ClientHello.random | ServerHello.random | ServerKeyExchange.curve_type | ServerKeyExchange.named_cuve | ServerKeyExchange.pubkey_length | ServerKeyExchange.pubkey
# m = a1fe224ab613179d0c166381230fcfedd50d6f7128177bf24a762f10129ee80df8e88488a3b474aa36913455ed30be9ce3133def8e7bb57c64768ac74f48fa7d
# h = sha512sum(m)[:256]
h = 0xa1fe224ab613179d0c166381230fcfedd50d6f7128177bf24a762f10129ee80d

G = E([Gx,Gy])
q = G.order()
assert(q == n)

w = mod(f2**(-1),q)
w1 = mod(h*w,q);
w2 = mod(f1*w,q);
v = Integer(w1)*G+Integer(w2)*P
print 'Correct signature?', mod(v[0],q) == f1


## Exercise 2 #################################################################
print '\n## Exercise 2 ###################################'

# Website: twitter.com

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
P = E([Px,Py])
assert(mod(Py**2,p)==mod(Px**3+a*Px+b,p))

G = E([Gx,Gy])
dni = 77620769

privkey = int(str(dni)*8)
pubkey = privkey * G
print 'pubkey:', pubkey

x = dni
z = mod(x**3+a*x+b,p)
assert(mod(z**((p-1)/2),p)==1)
y = mod(z**((p+1)/4),p)
Q = E([x,y])
assert(mod(y**2,p)==mod(x**3+a*x+b,p))
print 'Q:', Q

# We can't find the private key associated to the public key Q because 
# it's the Discrete Logarithm Problem, which is conjetured intractable
# print discrete_log(Q, G, G.order(), operation='+') # takes forever


## Exercise 3 #################################################################
print '\n## Exercise 3 ###################################'

CRL_URI = 'http://sr.symcb.com/sr.crl'
crl_file = urllib2.urlopen(CRL_URI)
crl_object = OpenSSL.crypto.load_crl(OpenSSL.crypto.FILETYPE_ASN1, crl_file.read())
crl_file.close()
revoked_objects = crl_object.get_revoked()
print 'CRL revoked certificates:', len(revoked_objects)

# curl http://sr.symcb.com/sr.crt > sr.crt
f = open('sr.crt','w')
subprocess.call(['curl','http://sr.symcb.com/sr.crt'],stdout=f)
# openssl x509 -in sr.crt -inform der -out sr.pem
subprocess.call(['openssl','x509','-in','sr.crt','-inform','der','-out','sr.pem'])
# cat SymantecClass3EVSSLCA-G3.crt VeriSignClass3PublicPrimaryCertificationAuthority-G5.crt > chain.crt
f = open('chain.crt','w')
subprocess.call(['cat','SymantecClass3EVSSLCA-G3.crt','VeriSignClass3PublicPrimaryCertificationAuthority-G5.crt'],stdout=f)
# openssl ocsp -issuer chain.crt -cert twitter.crt -url  http://sr.symcd.com -CAfile sr.pem
try:
	subprocess.check_output(['openssl','ocsp','-issuer','chain.crt','-cert','twitter.crt','-url','http://sr.symcd.com','-CAfile','sr.pem'])
except subprocess.CalledProcessError as e:
	print e.output