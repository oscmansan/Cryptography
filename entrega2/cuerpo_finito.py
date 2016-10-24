#!/usr/bin/python
from random import randint
from time import time

def GF_product_p(a, b):
	if a == 0 or b == 0: return 0

	p = 0
	while a:
		if a & 0x01:
			p ^= b
		a >>= 1
		b <<= 1
		if b & 0x100: # we exceed the rank
			b ^= 0x1B # x^8 mod (x^8+x^4+x^3+x+1) = x^4+x^3+x+1 = 0x1B

	return p & 0xFF

def GF_tables():
	exp = [0x01] # x^0 = 1
	while len(exp) < 256:
		exp.append(GF_product_p(exp[-1],0x03))

	log = [0] * 256
	for i,e in enumerate(exp):
		log[e] = i

	return exp, log

def GF_product_t(a, b):
	if a == 0 or b == 0: return 0

	x = log[a]
	y = log[b]

	return exp[(x+y)%255] & 0xFF

def GF_product_p_02(a):
	if a == 0: return 0

	p = a << 1
	if p & 0x100:
		p ^= 0x1B

	return p & 0xFF

def GF_product_t_02(a):
	if a == 0: return 0

	x = log[a]
	y = 0x19

	return exp[(x+y)%255] & 0xFF

def GF_product_p_03(a):
	if a == 0: return 0

	p = a << 1
	if p & 0x100:
		p ^= 0x1B
	p ^= a

	return p & 0xFF

def GF_product_t_03(a):
	if a == 0: return 0

	x = log[a]
	y = 0x01

	return exp[(x+y)%255] & 0xFF

def GF_product_p_09(a):
	if a == 0: return 0

	p = a << 3
	if p & 0x100:
		p ^= 0x1B
	if p & 0x200:
		p ^= 0x36
	if p & 0x400:
		p ^= 0x6C
	p ^= a

	return p & 0xFF

def GF_product_t_09(a):
	if a == 0: return 0

	x = log[a]
	y = 0xC7

	return exp[(x+y)%255] & 0xFF

def GF_product_p_0B(a):
	if a == 0: return 0

	p = a << 1
	if p & 0x100:
		p ^= 0x1B
	q = a << 3
	if q & 0x100:
		q ^= 0x1B
	if q & 0x200:
		q ^= 0x36
	if q & 0x400:
		q ^= 0x6C
	r = p ^ q ^ a

	return r & 0xFF

def GF_product_t_0B(a):
	if a == 0: return 0

	x = log[a]
	y = 0x68

	return exp[(x+y)%255] & 0xFF

def GF_product_p_0D(a):
	if a == 0: return 0

	p = a << 2
	if p & 0x100:
		p ^= 0x1B
	if p & 0x200:
		p ^= 0x36
	q = a << 3
	if q & 0x100:
		q ^= 0x1B
	if q & 0x200:
		q ^= 0x36
	if q & 0x400:
		q ^= 0x6C
	r = p ^ q ^ a

	return r & 0xFF

def GF_product_t_0D(a):
	if a == 0: return 0

	x = log[a]
	y = 0xEE

	return exp[(x+y)%255] & 0xFF

def GF_product_p_0E(a):
	if a == 0: return 0

	p = a << 1
	if p & 0x100:
		p ^= 0x1B
	q = a << 2
	if q & 0x100:
		q ^= 0x1B
	if q & 0x200:
		q ^= 0x36
	r = a << 3
	if r & 0x100:
		r ^= 0x1B
	if r & 0x200:
		r ^= 0x36
	if r & 0x400:
		r ^= 0x6C
	s = p ^ q ^ r

	return s & 0xFF

def GF_product_t_0E(a):
	if a == 0: return 0

	x = log[a]
	y = 0xDF

	return exp[(x+y)%255] & 0xFF

def GF_generador():
	gen = []

	all = set(range(1,256))

	for i in range(1,256):
		exp = [i]
		while len(exp) < 256:
			exp.append(GF_product_p(exp[-1],i))
		
		if all.issubset(set(exp)):
			gen.append(i)

	return gen

def GF_invers(a):
	if a == 0: return 0

	r = 255 - log[a] # a * (0x03)^r = (0x03)^255 = 1 mod (x^8+x^4+x^3+x+1)
	return exp[r]


#############################################################################

exp, log = GF_tables()

'''
exp = map(lambda x: '{:02x}'.format(x),exp)
for i in range(16):
	print ' '.join(exp[16*i:16*(i+1)])

print '\n'

log = map(lambda x: '{:02x}'.format(x),log)
for i in range(16):
	print ' '.join(log[16*i:16*(i+1)])
'''

for _ in range(100):
	a = randint(0,255)
	b = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	assert r1 == r2

b = 0x02
for _ in range(100):
	a = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	r3 = GF_product_p_02(a)
	r4 = GF_product_t_02(a)
	assert r1 == r2 == r3 == r4

b = 0x03
for _ in range(100):
	a = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	r3 = GF_product_p_03(a)
	r4 = GF_product_t_03(a)
	assert r1 == r2 == r3 == r4

b = 0x09
for _ in range(100):
	a = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	r3 = GF_product_p_09(a)
	r4 = GF_product_t_09(a)
	assert r1 == r2 == r3 == r4

b = 0x0B
for _ in range(100):
	a = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	r3 = GF_product_p_0B(a)
	r4 = GF_product_t_0B(a)
	assert r1 == r2 == r3 == r4

b = 0x0D
for _ in range(100):
	a = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	r3 = GF_product_p_0D(a)
	r4 = GF_product_t_0D(a)
	assert r1 == r2 == r3 == r4

b = 0x0E
for _ in range(100):
	a = randint(0,255)
	r1 = GF_product_p(a,b)
	r2 = GF_product_t(a,b)
	r3 = GF_product_p_0E(a)
	r4 = GF_product_t_0E(a)
	assert r1 == r2 == r3 == r4

#print GF_generador()

for _ in range(100):
	a = randint(1,255)
	b = GF_invers(a)
	assert GF_product_p(a,b) == 1


'''
n = 100000
a = []
b = []
for _ in range(n):
	a.append(randint(0,255))
	b.append(randint(0,255))

start = time()
for i in range(n):
	GF_product_p(a[i],b[i])
t = time() - start
print t

start = time()
for i in range(n):
	GF_product_t(a[i],b[i])
t = time() - start
print t
'''