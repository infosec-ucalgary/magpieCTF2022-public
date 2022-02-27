
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter
from ntru_encrypt import *

aes_key = b""


def get_pops_encryption():
	FLAG = "<redacted>"
	global aes_key

	aes_key = os.urandom(16)
	nonce = os.urandom(16)

	ctr = Counter.new(128, initial_value=int.from_bytes(nonce, "big"))
	cipher = AES.new(aes_key, AES.MODE_CTR, counter=ctr)

	ciphertext = cipher.encrypt(FLAG)

	return ciphertext, nonce


def get_pops_key(pubkey):
	global aes_key

	ntru_key = Ntru(509, 3, 2048, 226)
	ntru_key.set_pubkey(pubkey)

	# One time pad is a padding scheme ... right?
	pad = os.urandom(16)
	message_bytes = bytes([aes_key[i] ^ pad[i] for i in range(16)]) + pad

	checksum = hashlib.md5()
	checksum.update(message_bytes)
	message_bytes += checksum.digest()

	message = []
	for i in range(383, -1, -1):
		message.append((int.from_bytes(message_bytes, "big") >> i) & 1)

	# polynomial f represented as list c where f = c[0]x^0 + c[1]x^1 + ... + c[n]x^n
	return ntru_key.encrypt(message)
