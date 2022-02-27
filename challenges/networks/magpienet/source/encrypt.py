import sys
import time
import socket
import threading

def header():
    msg = """DEBUG: Stacktrace printing enabled. For production, set the production setting.
Auth Node: Enter whether you need encryption or decryption > """
    return msg

def respond():
    msg = """ERROR: module 'magpie_crypto', method 'RC2' expects 3 positional arguments (missing argument: 'input')
Exception in thread "main" magpie.lang.ModuleException: at ... file = RC2(key = "n3tw0rk1ng", iv = ""); [line 33]
"""
    return msg

def handle_user_connections(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    while True:
        try: 
            time.sleep(0.01)
            s.listen(1)
            csock, caddr = s.accept()
            t = ClientThread(csock, caddr)
            t.start()
        except RuntimeError as e:
            print(f"ERROR: (TOTAL THREADS: {threading.enumerate()}) - Runtime error - {e} ")

def handle_network_connection(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(b"JOIN")
    address = s.recv(1024).decode('utf-8').strip()
    print(f"LOG: Received address of {address}")
    msg = f"SETRETPORT {address.split('.')[1]} {sys.argv[2]}"
    s.send(msg.encode())
    msg = f"RENAME {address.split('.')[1]} encryption"
    s.send(msg.encode())
    while True:
        time.sleep(0.01)
        # Just wait here
        pass
    s.close()

class ClientThread(threading.Thread):
    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr

    def run(self):
        try:
            self.send(header())
            while True:
                time.sleep(0.01)
                data = self.sock.recv(1024).decode('utf-8').strip()
                if len(data) > 0:
                    self.send(respond())
                    break
            self.sock.close()
        except Exception as e:
            print(f"ERROR: {e}")

    def send(self, msg):
        self.sock.send(msg.encode())

if __name__ == "__main__":
    print("LOG: Starting encrypt/decrypt node")
    threads = []
    tu = threading.Thread(target=handle_user_connections, args=[int(sys.argv[2])])
    tn = threading.Thread(target=handle_network_connection, args=["srv3.momandpopsflags.ca", int(sys.argv[1])])
    threads.append(tu)
    threads.append(tn)
    tu.start()
    tn.start()
    for t in threads:
        t.join()
