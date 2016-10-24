#!/usr/bin/python
import aes
from random import randint
import matplotlib.pyplot as plt

def print_block(block):
	assert len(block) == 16, 'Invalid blocksize'
	block = map(lambda x: '{:02x}'.format(x),block)
	print ' '.join(block[0:4])
	print ' '.join(block[4:8])
	print ' '.join(block[8:12])
	print ' '.join(block[12:16])

def bytes_to_bits(bytes):
	bits = 0
	for byte in bytes:
		bits = bits<<8 | byte
	return bits

def bits_to_bytes(bits):
	bytes = []
	while bits:
		bytes.append(int(bits & 0xff))
		bits >>= 8
	return bytes[::-1]

def shift_bit(i, block):
	bits = bin(bytes_to_bits(block))[2:]
	bits = list('0'*(128-len(bits)) + bits)
	bits[i] = '0' if bits[i] == '1' else '1'
	bits = ''.join(bits)
	bits = int(bits, 2)
	bytes = bits_to_bytes(bits)
	return [0]*(16-len(bytes)) + bytes

def generateRandomBlock():
	block = []
	for _ in range(16):
		block.append(randint(0,255))
	return block

def countDifferentBits(A, B):
	A = bin(bytes_to_bits(A))[2:]
	A = list('0'*(128-len(A)) + A)
	B = bin(bytes_to_bits(B))[2:]
	B = list('0'*(128-len(B)) + B)

	n = 0
	for a,b in zip(A,B):
		if a != b:
			n += 1
	return n

def changedPositions(A, B):
	A = bin(bytes_to_bits(A))[2:]
	A = list('0'*(128-len(A)) + A)
	B = bin(bytes_to_bits(B))[2:]
	B = list('0'*(128-len(B)) + B)

	p = []
	for i,(a,b) in enumerate(zip(A,B)):
		if a != b:
			p.append(i)
	return p


# Canviem la funcio ByteSub per la identitat
def exercici_1a():
	K = generateRandomBlock()

	for _ in range(100):
		M = generateRandomBlock()

		i = randint(0,127)
		j = randint(0,127)
		k = randint(0,127)
		l = randint(0,127)
		
		Mi    = shift_bit(i,M)
		Mj    = shift_bit(j,M)
		Mk    = shift_bit(k,M)
		Ml    = shift_bit(l,M)
		Mij   = shift_bit(j,Mi)
		Mijk  = shift_bit(k,Mij)
		Mijkl = shift_bit(l,Mijk)

		C     = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci    = aes.encrypt(Mi, K, aes.keySize["SIZE_128"])
		Cj    = aes.encrypt(Mj, K, aes.keySize["SIZE_128"])
		Ck    = aes.encrypt(Mk, K, aes.keySize["SIZE_128"])
		Cl    = aes.encrypt(Ml, K, aes.keySize["SIZE_128"])
		Cij   = aes.encrypt(Mij, K, aes.keySize["SIZE_128"])
		Cijkl = aes.encrypt(Mijkl, K, aes.keySize["SIZE_128"])

		assert bytes_to_bits(C) == bytes_to_bits(Ci) ^ bytes_to_bits(Cj) ^ bytes_to_bits(Cij)
		assert bytes_to_bits(Cijkl) == bytes_to_bits(C) ^ bytes_to_bits(Ci) ^ bytes_to_bits(Cj) ^ bytes_to_bits(Ck) ^ bytes_to_bits(Cl)

# Canviem la funcio ShiftRows per la identitat
# Els xifrats C i Ci son identics excepte en una fila
def exercici_1b():
	K = generateRandomBlock()

	for _ in range(1):
		M = generateRandomBlock()

		i = randint(0,127)
		Mi = shift_bit(i,M)

		C  = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci = aes.encrypt(Mi, K, aes.keySize["SIZE_128"])

		print_block(C)
		print ''
		print_block(Ci)


# Canviem la funcio MixColumns per la identitat
# Els xifrats C i Ci son identics excepte en un byte
def exercici_1c():
	K = generateRandomBlock()

	for _ in range(1):
		M = generateRandomBlock()

		i = randint(0,127)
		Mi = shift_bit(i,M)

		C  = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci = aes.encrypt(Mi, K, aes.keySize["SIZE_128"])

		print_block(C)
		print ''
		print_block(Ci)

# Histograma del nombre total de bits que canvien amb cada modificacio de M
def exercici_2a():	
	M = generateRandomBlock()
	K = generateRandomBlock()
	hist = [0]*128
	for _ in range(100):
		i = randint(0,127)
		Mi = shift_bit(i,M)

		C  = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci = aes.encrypt(Mi, K, aes.keySize["SIZE_128"])

		hist[countDifferentBits(C,Ci)] += 1
	plt.bar(range(128),hist)
	plt.title('Nombre total de bits que canvien amb cada modificacio de M')
	plt.show()

# Histograma de les posicions que canvien amb cada modificacio de M
def exercici_2b():	
	M = generateRandomBlock()
	K = generateRandomBlock()
	hist = [0]*128
	for _ in range(100):
		i = randint(0,127)
		Mi = shift_bit(i,M)

		C  = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci = aes.encrypt(Mi, K, aes.keySize["SIZE_128"])

		pos = changedPositions(C,Ci)
		for p in pos:
			hist[p] += 1
	plt.bar(range(128),hist)
	plt.title('Posicions que canvien amb cada modificacio de M')
	plt.show()

# Histograma del nombre total de bits que canvien amb cada modificacio de K
def exercici_2c():	
	M = generateRandomBlock()
	K = generateRandomBlock()
	hist = [0]*128
	for _ in range(100):
		i = randint(0,127)
		Ki = shift_bit(i,K)

		C  = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci = aes.encrypt(M, Ki, aes.keySize["SIZE_128"])

		hist[countDifferentBits(C,Ci)] += 1
	plt.bar(range(128),hist)
	plt.title('Nombre total de bits que canvien amb cada modificacio de K')
	plt.show()

# Histograma de les posicions que canvien amb cada modificacio de K
def exercici_2d():	
	M = generateRandomBlock()
	K = generateRandomBlock()
	hist = [0]*128
	for _ in range(100):
		i = randint(0,127)
		Ki = shift_bit(i,K)

		C  = aes.encrypt(M, K, aes.keySize["SIZE_128"])
		Ci = aes.encrypt(M, Ki, aes.keySize["SIZE_128"])

		pos = changedPositions(C,Ci)
		for p in pos:
			hist[p] += 1
	plt.bar(range(128),hist)
	plt.title('Posicions que canvien amb cada modificacio de K')
	plt.show()


if __name__ == "__main__":
	aes = aes.AES()
	
	exercici_1a()
	#exercici_1b()
	#exercici_1c()
	#exercici_2a()
	#exercici_2b()
	#exercici_2c()
	#exercici_2d()