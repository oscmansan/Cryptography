#!/usr/bin/python
import struct
import magic
import binascii
from Crypto.Cipher import AES


# checks if the file has the correct PKCS7 padding
def check_padding(file):
	last_block = file[-16:]
	last_block = map(lambda byte: struct.unpack('B', byte)[0],last_block)
	k = last_block[-1] # last byte
	if k not in range(1,16): return False
	return last_block[-k:] == [k]*k


## Ejercicio 1 ######################################################

f = open('2016_10_10_17_00_19_oscar.manas.enc','rb')
cyphertext = f.read()
f.close()

f = open('2016_10_10_17_00_19_oscar.manas.key','rb')
cypherkey = f.read()
f.close()

iv = cyphertext[:16] # the initialization vector is prepended to the cyphertext
cyphertext = cyphertext[16:]

# we try each possible mode
for mode in [AES.MODE_ECB,AES.MODE_CBC,AES.MODE_CFB,AES.MODE_OFB]:
	aes = AES.new(cypherkey, mode, iv)
	message = aes.decrypt(cyphertext)
	#print str(mode) + ': ' + magic.from_buffer(message)
	if check_padding(message): print str(mode) + ': ' + binascii.hexlify(message[-16:])

# the mode that was used to encrypt the message is OFB
aes = AES.new(cypherkey, AES.MODE_OFB, iv)
message = aes.decrypt(cyphertext)
f = open('2016_10_10_17_00_19_oscar.manas.dec','wb')
f.write(message)
f.close()


## Ejercicio 2 ######################################################

f = open('2016_10_10_17_00_19_oscar.manas.puerta_trasera.enc','rb')
cyphertext = f.read()
f.close()

iv = cyphertext[:16] # the initialization vector is prepended to the cyphertext
cyphertext = cyphertext[16:]

# we try each possibility of the unknown byte kiv
for kiv in range(256):
	# we obtain the cypherkey by doing iv[i] ^ kiv, for i in [0..15]
	cypherkey = map(lambda byte: struct.unpack('B', byte)[0] ^ kiv, iv)
	cypherkey = struct.pack('B'*16, *cypherkey)
	aes = AES.new(cypherkey, AES.MODE_CBC, iv)
	message = aes.decrypt(cyphertext)
	#print "0x{:02x}".format(kiv) + ': ' + magic.from_buffer(message)
	if check_padding(message): print '0x{:02x}'.format(kiv) + ': ' + binascii.hexlify(message[-16:])

# the unknown byte is kiv = 0x45
kiv = 0x45
cypherkey = map(lambda byte: struct.unpack('B', byte)[0] ^ kiv, iv)
cypherkey = struct.pack('B'*16, *cypherkey)
aes = AES.new(cypherkey, AES.MODE_CBC, iv)
message = aes.decrypt(cyphertext)
f = open('2016_10_10_17_00_19_oscar.manas.puerta_trasera.dec','wb')
f.write(message)
f.close()