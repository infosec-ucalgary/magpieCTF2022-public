# Intercepting Mom and Pop's Flags Accounting Messages
### Category: Cryptography
### Author: Amna Adnan (amnaadnan11)

## Description
An accountant at Mom and Pops Flags sends a message regarding the company’s income statement to a newly established audit firm. The accountant converts each character of the message to ASCII Code and then encrypts each number using RSA encryption. You were able to intercept the ciphertext sent to the newly established auditing firm, whose public key was e = 13 and n = 527. The ciphertext was: 

C = 159 405 443 45 420 16 123 509 83 16 504 456 16 118 16 468 291 16 504 119 405 13 504 488 16 456 144 435. 

The flag is the message sent by the accountant at Mom and Pops flag to the newly established auditing company.

## Hints
1. Find the decryption key, remember d = e^-1 mod φ(n), which is equivalent to ed = 1 mod φ(n) or ed mod φ(n) = 1. 
2. Use the decryption key to decrypt each number to get the ASCII code for each character in the message sent.

## Solution
Given n = 527, by factoring we can determine that p = 17 and q = 31.

Then we calculate Euler’s Totient Function, φ(n) = (p-1)(q-1) = (17-1)(31-1) = (16)(30) = 480

We know that d = e^-1 mod φ(n), which is equivalent to ed = 1 mod φ(n) or ed mod φ(n) = 1. 

ed = 1 mod φ(n)

(13)(d) = 1 mod 480 

(13)(d) = 481

d = 37


Now that we have the private key, d = 37 and n = 527, we can determine the plaintext: 

Each character in the message was converted to ASCII code then encrypted using RSA encryption, therefore to get the message we can use the formula M = (C)^d mod n to decrypt each number given that we now know that d = 37 to obtain the ASCII code and then find the corresponding character in the message, for example: 

C = 159 405 443 45 420 16 123 509 83 16 504 456 16 118 16 468 291 16 504 119 405 13 504 488 16 456 144 435

To find the first character in the message we would:

First decrypt the number to find the ASCII code 

M = (C)^d mod n

M = (159)^37 mod 527 = 109 

Then find the character corresponding to that ASCII code, in this case the ASCII code, 109, corresponds to the character m. 

You can do this for each number to obtain the message or you can use calculators online where once you have found the decryption key d, you can enter the ciphertext and the decryption key to get the decrypted message and then convert the ASCII codes to characters. 

Both methods will result in finding the message: magpie{The\_revenue\_was\_zero}.   

## Flag
magpie{The\_revenue\_was\_zero}