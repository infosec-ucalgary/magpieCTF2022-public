from secrets import randbelow


def egcd(p, q):
	if q > p:
		p, q = q, p

	p_0, q_0 = 1, 0
	p_1, q_1 = 0, 1

	while q != 0:
		p_0, q_0, p_1, q_1 = p_1, q_1, p_0 - p_1*(p//q), q_0 - q_1*(p//q)
		p, q = q, p%q

	return p, p_0, q_0


def modinv(a, p):
	g, x, y = egcd(p, a)
	if g != 1:
		return False
	return y % p


def degree(f):
	d = len(f) - 1
	while d > 0:
		if f[d] != 0:
			break
		d -= 1
	return d


def trim(f):
	d = len(f) - 1
	while d > 0:
		if f[d] != 0:
			break
		d -= 1
	return f[:d+1]


def gen_ternary(n, d1, dn1):
	f = [0 for _ in range(n)]

	for i in range(d1):
		r = randbelow(n)
		while f[r] != 0:
			r = randbelow(n)

		f[r] = 1

	for i in range(dn1):
		r = randbelow(n)
		while f[r] != 0:
			r = randbelow(n)

		f[r] = -1

	return f


def add_poly(f, g):
	if len(f) < len(g):
		f, g = g, f

	h = f.copy()

	for i in range(len(g)):
		h[i] = h[i] + g[i]

	return h


def neg_poly(f):

	h = []
	for i in range(len(f)):
		h.append(-f[i])
	return h


def mult_poly(f, g, n):
	if len(f) == 0:
		f = [0]
	if len(g) == 0:
		g = [0]

	result = [0 for _ in range(max((len(f)-1)+(len(g)-1)+1, n))]
	for i in range(len(f)):
		for j in range(len(g)):
			result[i+j] += f[i] * g[j]

	if n > 0:
		for i in range(n, len(result), 1):
			result[i%n] += result[i]

		return result[:n]
	else:
		return result


def reduce_poly(f, q):

	h = []
	for i in range(len(f)):
		h.append(f[i] % q)

	return trim(h)


def center_poly(f, q):

	h = []
	for i in range(len(f)):
		h.append(f[i] % q)
		if h[i] > q//2:
			h[i] = h[i] - q

	return trim(h)


def div_poly(a, b, p):
	r = a.copy()
	q = [0]

	n = degree(b)
	u = modinv(b[n], p)

	d = degree(r)

	while d >= n and (d != 0 or r[0] != 0):
		v = reduce_poly(mult_poly([u * r[d]], [1 if (i == d-n) else 0 for i in range(d+1)], 0), p)
		r = reduce_poly(add_poly(r, neg_poly(mult_poly(v, b, 0))), p)
		q = reduce_poly(add_poly(q, v), p)
		d = degree(r)

	return q, r


def egcd_poly(a, b, p):
	a, b = a.copy(), b.copy()
	if degree(b) > degree(a):
		a, b = b, a

	a_0, b_0 = [1], [0]
	a_1, b_1 = [0], [1]

	zero = True
	for i in range(len(b)):
		zero = zero and (b[i] == 0)

	while not zero:
		q, r = div_poly(a, b, p)
		a_0, b_0, a_1, b_1 = a_1, b_1, reduce_poly(add_poly(a_0, neg_poly(mult_poly(a_1, q, 0))), p), reduce_poly(add_poly(b_0, neg_poly(mult_poly(b_1, q, 0))), p)
		a, b = b, r

		zero = True
		for i in range(len(b)):
			zero = zero and (b[i] == 0)

	return a_0, b_0, a


def invert_poly_prime(a, p, n):
	u, v, d = egcd_poly(a, [-1] + [1 if i==(n-1) else 0 for i in range(n)], p)

	if degree(d) == 0:
		return reduce_poly(mult_poly([modinv(d[0], p)], v, n), p)
	else:
		return False


def invert_poly_comp(a, m, p, e):
	e_1 = e
	b = invert_poly_prime(reduce_poly(a, p), p, m)
	if not b:
		return False

	n = 2
	while e > 0:
		b = reduce_poly(add_poly(mult_poly([2], b, m), neg_poly(mult_poly(a, mult_poly(b, b, m), m))), p**n)
		e = e // 2
		n = n * 2

	return reduce_poly(mult_poly(b, [1], m), p**e_1)

