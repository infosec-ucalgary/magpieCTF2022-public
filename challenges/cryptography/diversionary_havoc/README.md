# Diversionary Havoc
### Category: Cryptography
### Author: Braydon Willms

## Description

Mom and Pops are about to celebrate the grand opening of their new flag cloning shop, and what better way to sneak in and take the template flag than by being loud and stylish? (By setting off all of their fireworks early as a distraction, of course.) All we have to do is get access to the launch controls.

nc <ip> <port>

## Hints

1. I'm pretty sure g is a primitive root of p, but I wonder if g^a has as many powers?

## Solution

1. As the hint suggests, we want to see whether g^a is a primitive root. We can try to go about this a couple of ways: 
	1. Try raising g^a to increasing powers. We'll find that (g^a)^158 = 1 (mod p), and there are only 158 resulting values that repeat in a loop.
	2. We can also use the primitive root test. In this case, we need to factor p-1 first (as the challenge hints we might want to). This is an easy enough task for an online calculator like factor db, and the factorization is 2 * 79 * q where q is a large prime. We then calculate (g^a)^(2 * 79) % p, (g^a)^(2 * q) % p, and (g^a)^(79 * q) % p. (g^a)^(2 * 79) turns out to be 1. The fact that any of these turn out to be 1, or that the powers repeat in a cycle with length much less than p-1, tells us g^a is not a primitive root. Furthermore, we can use the results of these tests to our advantage.

2. There are a couple of ways to go from here. One is simple but takes a few tries, and one is more complex but exact. First, the simple method. Since we know the powers of g^a repeat in a cycle of length 158, there are only 158 possible values for g^(ab), and guessing a random power of g^a (such as 1) is successful with probability 1/158. Guessing repeatedly will eventually solve the challenge.

3. Given that the powers of g^a repeat in a cycle and (g^a)^158 = 1 (which either test tells us), we have <br>
(g^a)^158 = 1 (mod p) <br>
g^(158a) = 1 (mod p) <br>
158a = 0 (mod p-1) <br>
This follows from Fermat's little theorem and the fact that g is a primitive root of p. In other words, 158a is a multiple of p - 1 = 2 * 79 * q, or a is a multiple of (p-1)/(2 * 79) = q. Furthermore, we only care what a is mod p-1, so we only need to raise g to the power of 158 different multiples of q (or (p-1)/158 if we never factored) and check if it is equal to g^a. As it turns out, a = 3q. Knowing this, we can compute (g^b)^a (mod p), and the challenge is solved.

## Flag

magpie{l1tiN9\_U9\_7He\_D4yL1T\_5kY}
