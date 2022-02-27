# Sticky Note
### Category: Networks
### Author: Alex Tenney (alexxxii)

## Description
Snooping around the back room in Mom and Pop's Flag Shop you find an old, 90s style computer still logged in! There was a big file open with some crazy looking text. There was also a sticky note under the keyboard. I heard someone coming so I copied down what I found as quickly as I could.

I wonder if we could use them to ssh into the follow server as the user papa: <ip> 

## Hints

1. The sticky note is a password

## Solution

1. The Crazy Text is a RSA private key encoded with a Vigenere Cipher.
    * This cipher uses a key (or password) to encrypt text, and we find this on the sticky note. Since we know the key, we can decrypt the private RSA key
    * Cyberchef is a good option for this
2. Now we will have to put this new decoded key on our machine, and change the permissions to ensure it matches a real private key.
  `vim private_key`
    * paste in the decoded key
  `chmod 700 private_key` 
3. Now we can ssh into the server with the follow command
  `ssh -i private_key user@<ip>`
    * the -i indicates we want to use a different private key file than the deafult
4. Now we should be able to see `flag.txt` in our home directory after running the `ls` command. We can see the flag using the command:
    `cat flag.txt`

## Flag
magpie{d3c0d3d_209skf82}
