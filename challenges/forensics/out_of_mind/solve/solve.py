#!/usr/bin/python3
# solves the out-of-mind challenge

from pwn import remote

HOST = "172.17.0.2"
PORT = 59465

FLAG = "magpie{0u7_0f_$1gh7;)}"

def solve() -> bool:
    conn = remote(HOST, PORT)
    conn.send(b'\r\n')
    conn.recvline()
    return bytes(FLAG, "utf-8") in conn.recvline()

def main():
    print(solve())

if __name__ == "__main__": main()
