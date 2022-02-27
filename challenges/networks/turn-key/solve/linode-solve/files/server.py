import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import time
from Crypto.Cipher import AES
import binascii
from datetime import datetime
from prometheus_client import start_http_server, Gauge

HOST = "0.0.0.0"
PORT = 40863
PROMETHEUS_PORT = 47299
FLAG = "magpie{tH15_b3tT3R_f**k1n9_w0Rk_p0p...}"

flag_data = [
    {
        "iv": "",
        "key": "",
        "cipher": "",
        "time": 0
    },
    {
        "iv": "",
        "key": "",
        "cipher": "",
        "time": 0
    },
    {
        "iv": "",
        "key": "",
        "cipher": "",
        "time": 0
    }
]

START_TIME = datetime.now()

SUCCESS_ATTEMPTS = 0
TOTAL_ATTEMPTS = 0

FAIL_G = Gauge("turn_key_consecutive_fails", "Number of fails in a row for turn-key")
SUCCESS_G = Gauge("turn_key_consecutive_flags", "Number of times the flag was retrieved")
LAST_SOLVE_G = Gauge("last_successful_solve_epoch", "The last time, in epoch time, the flag was retrieved")

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode())

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        
        handle_json(message)
        self.send_response(200)
        self.end_headers()
        

def handle_json(message):
    print(message)

    server_id = int(message["id"])

    flag_data[server_id]["iv"] = message["iv"]
    flag_data[server_id]["key"] = message["key"]
    flag_data[server_id]["cipher"] = message["cipher"]
    flag_data[server_id]["time"] = get_ms_time()

    check_solve()

def solve():
    key = ""
    for data in flag_data:
        key += data["key"]

    unhex_key = binascii.unhexlify(key)
    unhex_iv = binascii.unhexlify(flag_data[0]["iv"])
    unhex_cipher = binascii.unhexlify(flag_data[0]["cipher"])

    flag = decrypt(unhex_key, unhex_iv, unhex_cipher)
    
    print(f"\033[92m{flag}\033[0m")

    f = open("/root/flag.txt", "w")
    f.write(str(datetime.now()) + "\n\n")
    f.write(flag + "\n")
    f.close()

    return flag.strip() == FLAG

def decrypt(key, iv, enc):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(enc).decode('utf-8')

def get_ms_time():
    return round(time.time() * 1000)

def check_solve():
    global START_TIME
    global SUCCESS_ATTEMPTS
    global TOTAL_ATTEMPTS
    global FAIL_G

    max_difference = 3000

    current_time = get_ms_time()    # ms.

    # Check times.
    for data in flag_data:
        if abs(current_time - data["time"]) > max_difference:
            return

    # Everything below here is a single call.

    TOTAL_ATTEMPTS += 1

    # Check data.
    iv = flag_data[0]["iv"]
    cipher = flag_data[0]["cipher"]
    
    valid_data = True
    for data in flag_data:
        if data["iv"] != iv:
            valid_data = False
            break

        if data["cipher"] != cipher:
            valid_data = False
            break

    if valid_data:
        SUCCESS_ATTEMPTS += 1
        if solve():
            SUCCESS_G.inc()
            LAST_SOLVE_G.set(int(datetime.now().strftime("%s")))
        else:
            SUCCESS_G.set(0)
        FAIL_G.set(0)
    else:
        print(f"\033[91mFAIL\033[0m")
        FAIL_G.inc()
        SUCCESS_G.set(0)

    percent = round(SUCCESS_ATTEMPTS / TOTAL_ATTEMPTS, 4) * 100
    runtime = datetime.now() - START_TIME

    print(f"\033[93mHit percentage: {percent}% in {str(runtime).split('.')[0]}\033[0m\n")

def main():
    server = HTTPServer((HOST, PORT), Server)

    start_http_server(PROMETHEUS_PORT)

    try:
        print(f"\033[94mStarting server on port {PORT}\033[0m\n")
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()

if __name__ == "__main__":
    main()
