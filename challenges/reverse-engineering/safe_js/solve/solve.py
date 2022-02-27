# Solves the Safe.js challenge
# Returns true if the flag is accessible

FLAG = "magpie{s0m3_08fusC@7i0n,_hvh}"
HOST = "localhost"
PORT = 8000

import requests
import json
import re

def solve() -> bool:
    data_json = requests.post(f"http://{HOST}:{PORT}/8d724b91d276b37b5e11080821a29624").content.decode("utf8")
    data = json.loads(data_json)

    gen_flag = ""
    for part in data["base"]:
        hex_val = hex(0xffffffff - part)
        for i in range(int(len(hex_val) / 2)):
            hex_part = hex_val[i*2:i*2+2]
            if hex_part == "0x": continue
            if hex_part == "00": continue
            gen_flag += chr(int(f"0x{hex_part}", 16))

    return FLAG == gen_flag
