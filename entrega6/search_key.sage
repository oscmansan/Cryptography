#!/usr/bin/env sage
import itertools

p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E = EllipticCurve(Zmod(p),[a,b])

G = E([Gx,Gy])
dni = 77620769

print math.log(G.order(),2)

range = lambda stop: iter(itertools.count().next, stop)
for r in range(G.order()):
	print r
	P = r*G
	if str(P).startswith(str(dni)):
		break
