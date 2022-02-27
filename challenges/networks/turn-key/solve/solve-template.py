#!/usr/bin/python

from pwn import *

def main():

    turn_key_0 = "144.126.212.211"
    turn_key_1 = "143.110.188.116"
    turn_key_2 = "188.166.53.154"

    print("Running turn-key_0")
    pwn(turn_key_0)

    print("Running turn-key_1")
    pwn(turn_key_1)

    print("Running turn-key_2")
    pwn(turn_key_2)

def pwn(IP, PORT="5555"):
    conn = remote(IP, PORT)

    line = conn.recvline()

    answer = "INITIALIZE CONNECTION\n"
    conn.send(answer.encode())

    line = conn.recvline()

    answer = "SEND FLAG\n"
    conn.send(answer.encode())

    line = conn.recvline()
    words = line.decode("utf-8")
    words = line.split()
    newline = "\n"
    answer = words[-1] + newline.encode()
    conn.send(answer)

    line = conn.recvall()
    print(line.decode("utf-8"))

    conn.close()

if __name__ == "__main__":
    main()
