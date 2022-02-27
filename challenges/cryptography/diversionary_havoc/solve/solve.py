from pwn import *

FLAG = "magpie{l1tiN9_U9_7He_D4yL1T_5kY}"
HOST = "127.0.0.1"
PORT = 20000


def solve():
	# open server connection
	conn = remote(HOST, PORT)

	# read in values
	for i in range(4):
		discard = conn.recvline()

	gb = int(conn.recvline().decode('utf-8').split()[-1])

	for i in range(2):
		discard = conn.recvline()

	g = int(conn.recvline().decode('utf-8').split()[-1])
	p = int(conn.recvline().decode('utf-8').split()[-1])
	ga = int(conn.recvline().decode('utf-8').split()[-1])

	for i in range(2):
		discard = conn.recvline()

	# determine a (this assumes we have determined a is a multiple of q, here for demonstration)
	q = (p - 1)//158

	a = 0
	for i in range(158):
		a = i*q
		if pow(g, a, p) == ga:
			break

	# calculate and send shared secret
	gab = pow(gb, a, p)

	conn.sendline(str(gab))

	if FLAG in conn.recvline().decode('utf-8'):
		conn.close()
		return True
	else:
		conn.close()
		return False
