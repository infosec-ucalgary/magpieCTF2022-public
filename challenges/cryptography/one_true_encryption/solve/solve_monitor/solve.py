from pwn import *
from Crypto.Cipher import AES
from Crypto.Util import Counter
from prometheus_client import start_http_server, Gauge

FLAG = "magpie{0n3_TRU3_F149_C0Mp4nY_4ll_h41L_0mn1_7lag5}"
HOST = "srv3.momandpopsflags.ca"
PORT = 31337

BRUTE_FORCE_BITS = 20

FAIL_G = Gauge("one_true_encryption_fails",
        "number of failures of challenge one_true_encryption")
CRASH_G = Gauge("one_true_encryption_crash",
        "number of consecutive solve script crashes")

def solve():
	conn = remote(HOST, PORT)

	bits_found = 0
	known_aes_key = 0
	add_values = [[1, -1, 1], [1, 1, 0], [-1, 1, 1], [-1, -1, 0]]
	add_index = 0

	# Read in AES encryption of flag and nonce
	discard = conn.recvline()
	flag_ciphertext = bytes.fromhex(conn.recvline().decode('UTF-8').split()[-1])
	nonce = bytes.fromhex(conn.recvline().decode('UTF-8').split()[-1])

	for i in range(2):
		discard = conn.recvline()

	# Read in ntru encrypt parameters (Not that we really need to save them)
	n = int(conn.recvline().decode('UTF-8').split()[-1])
	p = int(conn.recvline().decode('UTF-8').split()[-1])
	q = int(conn.recvline().decode('UTF-8').split()[-1])

	# Read first ntru public key
	last_pubkey = conn.recvline().decode('UTF-8').split(':')[-1]

	while bits_found < 128-BRUTE_FORCE_BITS:
		print(bits_found)
		# Parse ciphertext into list
		ciphertext_string = conn.recvline().decode('UTF-8').split(':')[-1].strip()
		ciphertext = list(map(int, ciphertext_string.replace('[', '').replace(']', '').replace(' ', '').split(',')))

		discard = conn.recvline()

		# Take advantage of ntru homomorphism to add chosen values to the message polynomial
		ciphertext[bits_found] = (ciphertext[bits_found] + add_values[add_index][0]) % q
		ciphertext[bits_found + 128] = (ciphertext[bits_found + 128] + add_values[add_index][1]) % q
		conn.sendline(str(ciphertext).encode('UTF-8'))

		pubkey = conn.recvline().decode('UTF-8').split(':')[-1]

		# If both modified coefficients are still 0 or 1, we know the corresponding aes key bit
		if pubkey == last_pubkey:
			known_aes_key |= add_values[add_index][2] << (127-bits_found)
			bits_found += 1

		last_pubkey = pubkey

		add_index = (add_index + 1) % 4

	# Brute force last AES key bits to save time on network latency
	for guess in range(2**BRUTE_FORCE_BITS):
		aes_key = known_aes_key | guess

		ctr = Counter.new(128, initial_value=int.from_bytes(nonce, "big"))
		cipher = AES.new(aes_key.to_bytes(16, "big"), AES.MODE_CTR, counter=ctr)

		decrypted_flag = cipher.decrypt(flag_ciphertext)

		if b"magpie{" in decrypted_flag:
			conn.close()
			return FLAG in decrypted_flag.decode('UTF-8')

	conn.close()
	return False

def main():
    start_http_server(33433)
    while True:
        print("[info] starting solve script...")
        try:
            if solve():
                FAIL_G.set(0)
                print("[done] success!")
            else:
                FAIL_G.inc()
                print("[done] fail :(")
            
            CRASH_G.set(0)
        except Exception as e:
            CRASH_G.inc()
            print("[done] crash :((")

    return

if __name__ == "__main__": main()
