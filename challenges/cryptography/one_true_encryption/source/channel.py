

from mysterious_server import *
from flag_storage_client import *


def main():

	print("???: You don't get payed for nothing, Pops. "
							"We're going to need the new access code for that flag storage building.")

	flag_ciphertext, nonce = get_pops_encryption()

	print("Pop: Here's the access flag, encrypted with AES and everything: " + flag_ciphertext.hex())
	print("Pop: And the nonce: " + nonce.hex())

	send_server_flag(flag_ciphertext, nonce)

	pubkey = gen_server_pubkey()
	print("???: Good, but I also need the AES key. Encrypt it with that post-quantum secure scheme.")
	print("???: Here are the parameters:")
	print("N = 509")
	print("p = 3")
	print("q = 2048")
	print("???: Here's my public key: " + str(pubkey))

	ciphertext = get_pops_key(pubkey)

	print("Pop: Okay, here it is: " + str(ciphertext))
	print("Enter the ciphertext to send:", flush=True)
	ciphertext = input().strip().replace(" ", "").replace("[", "").replace("]", "")
	ciphertext = list(map(int, ciphertext.split(",")))

	success, pubkey = send_server_encryption(ciphertext)

	while not success:
		print("???: I think you messed it up. Try again with this key: " + str(pubkey))

		ciphertext = get_pops_key(pubkey)

		print("Pop: Okay, here it is: " + str(ciphertext))
		print("Enter the ciphertext to send:", flush=True)
		ciphertext = input().strip().replace(" ", "").replace("[", "").replace("]", "")
		ciphertext = list(map(int, ciphertext.split(",")))

		success, pubkey = send_server_encryption(ciphertext)

	print("???: Looks right. That's enough for now.", flush=True)


main()

