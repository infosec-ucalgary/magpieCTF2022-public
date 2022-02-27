#!/usr/bin/env python3
# Solves the Compare and Contrast magpieCTF-2022 challenge.
import requests
import json

HOST = "127.0.0.1"
PORT = 8000
FLAG = "magpie{|\/|ix1ng_|\|umb3r$_t0g3t43r}"

def solve() -> bool:
    data = {
        "answer": "omniflags stole all control"
    }

    resp = requests.post(f"http://{HOST}:{PORT}/check-plain", json=data).json()
    message_buff = resp["message"]["data"]

    message = ""

    for char_code in message_buff:
        message += chr(char_code)

    return FLAG in message

if __name__ == "__main__":
    print(solve())
