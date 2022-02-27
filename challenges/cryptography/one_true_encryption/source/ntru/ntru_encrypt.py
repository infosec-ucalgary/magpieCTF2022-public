import math
import secrets
from polynomial import *


class Ntru:

	def __init__(self, n, p, q, d_f):
		self.n = n
		self.p = p
		self.q = q
		self.d_f = d_f
		self.d_g = n // 3

	def gen_key(self):
		while True:
			F = gen_ternary(self.n, self.d_f//2, self.d_f//2)
			self.f = add_poly([1], mult_poly([self.p], F, self.n))
			self.f_q = invert_poly_comp(self.f, self.n, 2, int(math.log2(self.q)))
			if self.f_q:
				break

		self.g = gen_ternary(self.n, self.d_g, self.d_g)
		self.h = reduce_poly(mult_poly(mult_poly([self.p], self.f_q, self.n), self.g, self.n), self.q)

	def get_pubkey(self):
		return self.h

	def set_pubkey(self, h):
		self.h = h

	def encrypt(self, m):
		r = [secrets.randbelow(self.p) - self.p//2 for i in range(self.n)]
		ciphertext = reduce_poly(add_poly(mult_poly(r, self.h, self.n), m), self.q)
		return ciphertext + [0] * (self.n - len(ciphertext))

	def decrypt(self, e):
		a = center_poly(mult_poly(self.f, center_poly(e, self.q), self.n), self.q)
		plaintext = reduce_poly(a, self.p)
		return plaintext + [0] * (self.n - len(plaintext))
