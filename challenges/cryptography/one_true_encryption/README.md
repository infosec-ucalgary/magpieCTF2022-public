# One True Encryption
### Category: Cryptography
### Author: Braydon Willms

## Description

We managed to follow Pop to a new secure flag storage facility, and it looks like there's an encrypted line 
running to the building! Maybe you could tap it to mess with Pop's messages and find a way in...

nc &lt; ip &gt; &lt; port &gt;

## Hints

1. I wonder if the cryptosystem they're using has any useful properties...

## Solution 

1. There's quite a bit of code here, and first we'll want to figure out what it's actually doing. 
   1. We can see that the flag is first encrypted with AES in CTR mode, and we're given the ciphertext and nonce.
   2. After this, the server generates an "ntru key" and shares the public key.
   3. Now, we have a loop. First the client xors the AES key with a random value and tacks the random value on,
   as a sort of "one time pad padding scheme". It then computes an md5 checksum over this value and appends it.
   Finally, it converts the bits to 0 or 1 polynomial coefficients and encrypts the entire thing using the ntru public key.
   4. We're given a chance to change the message before the server decrypts it.
   5. The server decrypts with the ntru key, then checks that the coefficients are 0 and 1 before converting to binary.
   It then verifies the checksum, XORs the values to get the AES key back, 
    and checks that the AES decryption contains a flag. If something is wrong, a new AES key encryption is sent.
2. Next, we can look up the ntru encryption scheme used. This is a lattice based cryptosystem.
Basically, the message is represented as a polynomial m, and the encryption will be a polynomial of the form r*h+m,
where r is a random polynomial and h is the public key. This scheme is also additively homomorphic, meaning 
we can add two ciphertexts and the decryption will be the sum of the messages. Since r may be 0, a message is a valid
encryption of itself.
3. There is also an information leak in the server decryption function. Normally, the public key stays the same,
but a new one is generated if any of the decrypted coefficients are not 0 or 1.
We can use this to leak bits of the AES key - though we need both the padded bit and what it was XORed with to do this.
If we add a 1 and the key is unchanged, the original bit must have been 0.
If we can subtract 1 without changing the value to something besides 0 or 1, the original bit must have been 1.
4. To figure out the exact inputs, we can see what happens if we add certain values to certain message values.
The underlying encrypted values are on the left, and the values added by the attacker are on top.

|     | 1, 1 | 1, -1 | -1, 1 | -1, -1 |
|-----|------|-------|-------|--------|
| 0,0 | 1,1  | 1,-1  | -1,1  | -1,-1  |
| 0,1 | 1,2  | 1,0   | -1,2  | -1,0   |
| 1,0 | 2,1  | 2,-1  | 0,1   | 0,-1   |
| 1,1 | 2,2  | 2,0   | 0,2   | 0,0    |

We see that each added value in the top row only results in values that will not cause a key change in one case.
So, we can try adding these values to a bit and the corresponding pad bit, and when the ntru key does not change
we have found a bit in the aes key. We can repeat this process until we have the entire AES key, and finally
use that to decrypt the flag.

## Flag

magpie{0n3_TRU3_F149_C0Mp4nY_4ll_h41L_0mn1_7lag5}