#!/usr/bin/env python
import hashlib

files = ['ClientHello.random','ServerHello.random','ServerKeyExchange.curve_type',
		 'ServerKeyExchange.named_curve', 'ServerKeyExchange.pubkey_length', 
		 'ServerKeyExchange.pubkey']

m = ''
for fn in files:
	with open(fn,'r') as f:
		m += f.read()

def digest512():
	return int(hashlib.sha512(m).hexdigest(), 16)>>256

def digest256():
	return int(hashlib.sha256(m).hexdigest(), 16)

def digest1():
	return int(hashlib.sha1(m).hexdigest(), 16)

def digest():
	return digest1()