import socket

HOST = "srv3.momandpopsflags.ca"
PORT = 49988
FLAG = "magpie{n0_n33d_t0_r31nv3nt_th3_wh33l}"

def solve() -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(1024)
    s.send(b"AA00 TD92 PA29 AB41 AA01 AN02 MB58 AM01 AA00")
    flag_received = s.recv(1024).decode('utf-8').strip()
    return FLAG == flag_received.split(" ")[-1]

if __name__ == "__main__":
    print(solve())
