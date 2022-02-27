
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter
from ntru_encrypt import *

flag_enc = ""
aes_nonce = ""
ntru_key = None


def send_server_flag(flag_ciphertext, nonce):
	global flag_enc
	global aes_nonce

	flag_enc = flag_ciphertext
	aes_nonce = nonce

	return


def gen_server_pubkey():
	global ntru_key
	ntru_key = Ntru(509, 3, 2048, 226)

	ntru_key.gen_key()

	return ntru_key.get_pubkey()


def send_server_encryption(ciphertext):
	global flag_enc
	global aes_nonce
	global ntru_key

	# polynomial f represented as list c where f = c[0]x^0 + c[1]x^1 + ... + c[n]x^n
	message = ntru_key.decrypt(ciphertext)

	# Make sure the decryption represents binary values and generate a new key if not to be safe
	valid = True
	for i in range(len(message)):
		valid = valid and (message[i] in [0, 1])

	if not valid:
		return False, gen_server_pubkey()

	message_int = 0
	for i in range(384):
		message_int |= (message[383-i] << i)
	message_bytes = message_int.to_bytes(48, "big")
	message_bytes, checksum = message_bytes[:32], message_bytes[32:]

	md5hash = hashlib.md5()
	md5hash.update(message_bytes)

	if checksum != md5hash.digest():
		return False, ntru_key.get_pubkey()

	aes_key = bytes([message_bytes[i] ^ message_bytes[i+16] for i in range(16)])

	ctr = Counter.new(128, initial_value=int.from_bytes(aes_nonce, "big"))
	cipher = AES.new(aes_key, AES.MODE_CTR, counter=ctr)

	flag = cipher.decrypt(flag_enc)

	if b"magpie{" in flag:
		return True, ntru_key.get_pubkey()

	return False, ntru_key.get_pubkey()
