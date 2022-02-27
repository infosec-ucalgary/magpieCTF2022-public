from pwn import *
import sys
from datetime import datetime
import requests

def main():

    server_id = sys.argv[1]
    challenge_ip = sys.argv[2]
    solve_host = sys.argv[3]

    key, iv, cipher = pwn(challenge_ip)

    send_result(server_id, solve_host, key, iv, cipher)

    
def send_result(server_id, solve_host, key, iv, cipher):
    data = {
        "id": server_id,
        "iv": iv,
        "key": key,
        "cipher": cipher
    }

    requests.post(solve_host, json=data)


def save_result(result):
    f = open("/root/out.txt", "w")
    f.write(str(datetime.now()) + "\n\n")
    f.write(result)
    f.close()

def pwn(IP, PORT="5555"):
    conn = remote(IP, PORT)

    line = conn.recvline()

    answer = "INITIALIZE CONNECTION\n"
    conn.send(answer.encode())

    line = conn.recvline()

    answer = "SEND FLAG\n"
    conn.send(answer.encode())

    line = conn.recvline()
    words = line.split()
    newline = "\n"
    answer = words[-1] + newline.encode()
    conn.send(answer)

    line = conn.recvall()
    result = line.decode("utf-8")

    conn.close()

    save_result(result)

    s = result.split("\n")
    key = s[4][21:]
    iv = s[5][6:]
    cipher = s[6][14:]

    return (key, iv, cipher)

if __name__ == "__main__":
    main()

