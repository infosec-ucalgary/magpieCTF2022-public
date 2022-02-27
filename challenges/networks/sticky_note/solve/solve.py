import os
import paramiko

FLAG = "magpie{d3c0d3d_209skf82}"

HOST = "localhost"
PORT = 2222

def solve() -> bool:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(HOST, port=PORT, username="papa", key_filename="decrypted_key")

    stdin, stdout, stderr = client.exec_command("cat ./flag.txt")

    got_flag = stdout.read().decode("utf-8").rstrip("\n")

    return got_flag == FLAG

if __name__ == "__main__":
    solve()