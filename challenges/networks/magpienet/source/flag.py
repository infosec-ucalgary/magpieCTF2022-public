import sys
import time
import socket
import threading

FLAG = "magpie{n0_n33d_t0_r31nv3nt_th3_wh33l}"

# Graph Vertex Port numbers
#             0      1     2    3     4     5      6     7
PORT_LIST = [46442,46487,46441,46301,46316,46102,46911,46382]

# Graph Vertex Names
#               0       1       2       3       4       5       6       7
RADDR_LIST = ["AA00", "AA01", "AN02", "AM01", "PA29", "MB58", "AB41", "TD92"]

# E.g., the EDGES of the graph
NEIGHBOUR_LIST = set([(0,3),(0,7),(7,4),(7,3),(4,6),(6,1),(6,2),(1,2),(1,5),(2,5),(5,3)])

def handle_network_connection(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(b"JOIN")
    address = s.recv(1024).decode('utf-8').strip()
    print(f"LOG: Received address of {address}")
    msg = f"SETRETPORT {address.split('.')[1]} {int(sys.argv[2])}"
    print(f"SENDING: {msg}")
    s.send(msg.encode())
    msg = f"RENAME {address.split('.')[1]} flag"
    s.send(msg.encode())
    while True:
        time.sleep(0.01)
        # Just wait here
        pass
    s.close()

def has_edge(v1, v2):
    for n in NEIGHBOUR_LIST:
        v1_first = (RADDR_LIST.index(v1), RADDR_LIST.index(v2))
        v2_first = (RADDR_LIST.index(v2), RADDR_LIST.index(v1))
        if v1_first in NEIGHBOUR_LIST or v2_first in NEIGHBOUR_LIST:
            return True
    return False

def check_hamiltonian(user_input):
    print(f"CHECKING for Hamiltonian cycle for: {user_input}")
    nodes_checked = []
    input_list = user_input.split(" ")

    if len(input_list) != len(RADDR_LIST) + 1:
        return False

    if input_list[0] != input_list[-1]:
        return False

    for i in range(len(input_list)):
        n = input_list[i]
        if not n in RADDR_LIST:
            return False

        if n in nodes_checked and i != len(input_list):
            return False

        if i < len(input_list) - 1:
            if not has_edge(input_list[i], input_list[i+1]):
                return False

    return True

def handle_user_connections(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    print(f"LOG: Listening for users on port {port}")
    while True:
        time.sleep(0.01)
        server.listen(1)
        conn, addr = server.accept()
        conn.send(b"> ")
        data = conn.recv(1024).decode("utf-8").strip()
        if check_hamiltonian(data):
            msg = f"Congratulations! Here is the flag: {FLAG}"
            conn.send(msg.encode())
        else:
            conn.send(b"No")
        conn.close()

if __name__ == "__main__":
    print(f"LOG: Starting flag server")
    threads = []
    tu = threading.Thread(target=handle_user_connections, args=[int(sys.argv[2])])
    tn = threading.Thread(target=handle_network_connection, args=["srv3.momandpopsflags.ca", int(sys.argv[1])])
    threads.append(tu)
    threads.append(tn)
    tn.start()
    tu.start()
    for t in threads:
        t.join()
