import sys
import time
import socket
import threading

# PORT=46442
NODE = None
PORT_LIST = [46442,46487,46441,46301,46316,46102,46911,46382]
RADDR_LIST = ["AA00", "AA01", "AN02", "AM01", "PA29", "MB58", "AB41", "TD92"]
NEIGHBOUR_LIST = set([(0,3),(0,7),(7,4),(7,3),(4,6),(6,1),(6,2),(1,2),(1,5),(2,5),(5,3)])
PORT = PORT_LIST[int(sys.argv[2])]

# Check all arguments
def check_args():
    """
    python node.py <port> <order>
    """
    global PORT
    if len(sys.argv) != 2:
        print(f"LOG: No argument provided. Defaulting to {PORT}")
        return False
    else:
        try:
            PORT = int(sys.argv[1])
            if PORT < 1024:
                raise Exception
            return True
        except Exception:
            print("ERROR: Provided port must be greater than 1024")
            sys.exit(-1)

class HandleThread(threading.Thread):
    def __init__(self, caddr, csock):
        threading.Thread.__init__(self)
        self.caddr = caddr
        self.csock = csock
        self.identifier = -1  # If JOIN is used
        self.searchlog = []  # Hold search ID's to stop infinite loops

    def run(self):
        print(f"LOG: Connection from {self.caddr}")
        try:
            while True:
                time.sleep(0.01)
                data = self.csock.recv(1024).decode("utf-8").strip()
                if len(data) > 0:
                    self.handle_msg(data)
            self.csock.close()
        except ConnectionResetError:
            print(f"LOG: {self.caddr} disconnected")
            print(f"LOG: Removing {self.ident} from residents list")
            if self.identifier != -1:
                NODE.del_resident(self.identifier)
                self.identifier = -1
        except ConnectionAbortedError:
            print(f"LOG: {self.caddr} aborted connection")
            print(f"LOG: Removing {self.ident} from residents list")
            if self.identifier != -1:
                NODE.del_resident(self.identifier)
                self.identifier = -1
        except Exception as e:
            print(f"EXCEPTION: {e}")
            print(f"LOG: Removing {self.identifier} from residents list")
            if self.identifier != -1:
                NODE.del_resident(self.identifier)
                self.identifier = -1
            self.csock.send(b"ERROR: An error occured, you have been removed from the network.\n")
        self.csock.close()

    def send(self, msg):
        print(f"LOG: Sending {msg}")
        self.csock.send(msg.encode())

    def set_identifier(self, new_id):
        self.identifier = new_id

    def handle_msg(self, msg):
        global NODE
        if msg == "JOIN":
            if self.identifier == -1:
                new_num = NODE.get_res_count() + 1  # Start at 1 since router is 0
                new_addr = f"{NODE.address}.{new_num}"
                # IP. Socket port, resident number, resident name, open port (for connections)
                ip_to_use = self.caddr[0]
                if ip_to_use.split(".")[0].strip() == "10":
                    ip_to_use = "srv3.momandpopsflags.ca"
                new_res = (ip_to_use, self.csock.getpeername()[1], new_num, "default", -1)
                self.identifier = new_num
                NODE.add_resident(new_res)
                self.send(f"{new_addr}\n")
            else:
                self.send("ERROR: You are already a part of this network.\n")
        elif msg[0:10] == "SETRETPORT": # SETRETPORT <res no> <port>
            splits = msg[11:].strip().split(" ")
            print(f"LOG: Setting return port of {splits[0]} to {splits[1]}")
            NODE.set_resident_ret_port(int(splits[0]), int(splits[1]))
        elif msg == "LEAVE":
            if self.identifier != -1:
                print(f"LOG: Removing {self.ident} from residents list")
                NODE.del_resident(self.identifier)
                self.identifier = -1
            else:
                self.send("ERROR: You are not joined to this network\n")
        elif msg == "TRACE":
            if self.identifier != -1:
                self.send("USAGE: TRACE < addr | name >\n")
            else:
                self.send("ERROR: You are not joined to this network\n")
        elif msg == "PING":
            if self.identifier != -1:
                self.send("USAGE: PING < addr | name >")
            else:
                self.send("ERROR: You are not joined to this network\n")
        elif msg[0:4] == "PING":  # PING <ident>
            if self.identifier != -1:
                to_find = msg[5:].strip()
                found = NODE.has_resident(to_find)
                foundnb = NODE.has_neighbour(to_find)
                if found:
                    node_found = NODE.get_resident_tuple(to_find)
                    if node_found[1] == -1:
                        msg = f"SUCCESS {to_find} (IP={node_found[0]}, PORTS=n/a, Name={node_found[2]}) is a resident of this network\n"
                    else:
                        msg = f"SUCCESS {to_find} (IP={node_found[0]}, PORTS={node_found[1]}, Name={node_found[2]}) is a resident of this network\n"
                elif not found and foundnb:
                    msg = f"SUCCESS {to_find} {NODE.get_neighbour_tuple(to_find)} is a neighbouring router\n"
                else:
                    msg = f"FAILURE {to_find} not found in resident list or neighbour list for {NODE.address}\n"
                self.send(msg)
            else:
                self.send("ERROR: You are not joined to this network\n")
        elif msg[0:5] == "TRACE":
            if self.identifier != -1:
                to_find = msg[5:].strip()
                if NODE.has_resident(to_find):
                    ad = f"{NODE.address}\n"
                    self.send(ad)
                else:
                    self.send(f"ERROR: Could not find address {to_find} on this network ({NODE.address}). Please check with neighbouring routers: {NODE.get_neighbours()}\n")
            else:
                self.send("ERROR: You are not joined to this network\n")
        elif msg[0:7] == "ROUTING":  # TODO: DEBUG ONLY, REMOVE BEFORE CTF
            password = msg.split(" ")[1].strip()
            if password == "<PASSWORD>":
                self.send(f"Router({NODE.address}) - {NODE.neighbours}\n")
        elif msg[0:9] == "RESIDENTS":  # TODO: DEBUG ONLY, REMOVE BEFORE CTF
            password = msg.split(" ")[1].strip()
            if password == "<PASSWORD>":
                self.send(f"Router({NODE.address}) - {NODE.residents}\n")
        elif msg[0:7] == "ADDRESS":
            addr = msg[8:].strip()
            print(f"LOG: Setting address to {addr}")
            NODE.set_address(addr)
            self.send("OK")  # Address is set before neighbours
        elif msg[0:10] == "NEIGHBOURS":
            nhbs = eval(msg[11:].strip())
            to_add = [ eval(n) for n in nhbs ]  # They're sent as individual strings of tuples
            print(f"LOG: Setting neighbours to {to_add}")
            NODE.set_neighbours(to_add)
        elif msg[0:6] == "RENAME":
            if self.identifier != -1:
                splits = msg[7:].strip().split(" ")
                print(f"LOG: Setting name of {splits[0]} to {splits[1]}")
                NODE.set_resident_name(int(splits[0]), splits[1])
            elif self.identifier != int(splits[0]):
                self.send("ERROR: You cannot change another nodes name\n")
        else:
            self.send(f"ERROR: Unkown command {msg}\n")

    def get_config(self, config):
        # Theres no need for residents to be configured
        # They will be added when they connect to the router
        print(f"LOG: new routing config: {NODE}")

class Router():
    """
    Main routing class for each node
    """
    def __init__(self):
        self.address = "_"  # Default is '_' which is non-initialized
        self.identifier = "0"  # Much like the host IP section, where self.address is the network portion
        self.neighbours = []  # Routing neighbours  -  (IP, port, address)
        self.residents = []  # Nodes joined to this routers network  -  (IP, port, Resident obj)

    def set_neighbours(self, nbs):
        self.neighbours = nbs

    def set_address(self, addr):
        self.address = addr

    def has_resident(self, res):
        for r in self.residents:
            if str(r[2]) == str(res) or str(r[3]) == res:
                return True
        return False

    def has_neighbour(self, nb):
        for n in self.neighbours:
            if n[2] == nb:
                return True
        return False

    def get_resident_tuple(self, addr):
        for n in self.residents:
            if str(n[2]) == str(addr) or str(n[3]) == str(addr):
                return (n[0], n[4], n[3])
        return ("", -1)

    def get_neighbour_tuple(self, addr):
        for n in self.neighbours:
            if n[2] == addr:
                return (n[0], n[1])
        return ("", -1)

    def get_res_count(self):
        return len(self.residents)

    def set_resident_name(self, no, name):
        for i in range(len(self.residents)):
            if self.residents[i][2] == no:
                tup = self.residents[i]
                self.residents[i] = (tup[0], tup[1], tup[2], name, tup[4])


    def set_resident_ret_port(self, no, port):
        for i in range(len(self.residents)):
            if self.residents[i][2] == no:
                tup = self.residents[i]
                self.residents[i] = (tup[0], tup[1], tup[2], tup[3], port)

    def add_resident(self, res):
        self.residents.append(res)

    def del_resident(self, res):
        # res -> integer
        for r in self.residents:
            print(r)
            if r[2] == res:
                del self.residents[self.residents.index(r)]

    def get_neighbours(self):
        msg = ""
        for n in self.neighbours:
            msg += f"{n[2]} "
        return msg

    def __str__(self):
        return f"Router {PORT} {self.neighbours} {self.residents} {self.chunk}"

    def __repr__(self):
        return f"Router {PORT} {self.neighbours} {self.residents} {self.chunk}"

# Connect to manager and let it know this is a node
def init_connect(p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("srv3.momandpopsflags.ca", 42069))
    cmd = f"INIT {p}"
    s.send(cmd.encode())
    s.close()

# Main socket loop
def loop_listen():
    global PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    while True:
        try:
            server.listen(1)
            clientsock, clientaddr = server.accept()
            clientsock.settimeout(60)
            t = HandleThread(clientaddr, clientsock)
            t.start()
        except RuntimeError as e:
            print(f"ERROR: (TOTAL THREADS: {threading.enumerate()}) - Runtime error - {e} ")

def set_up_neighbours():
    nbs = []
    for n in NEIGHBOUR_LIST:
        if n[0] == int(sys.argv[2]) and ("srv3.momandpopsflags.ca", PORT_LIST[n[1]], RADDR_LIST[n[1]]) not in nbs:
            nbs.append(("srv3.momandpopsflags.ca", PORT_LIST[n[1]], RADDR_LIST[n[1]]))
        elif n[1] == int(sys.argv[2]) and ("srv3.momandpopsflags.ca", PORT_LIST[n[0]], RADDR_LIST[n[0]]) not in nbs:
            nbs.append(("srv3.momandpopsflags.ca", PORT_LIST[n[0]], RADDR_LIST[n[0]]))
    return nbs

if __name__ == "__main__":
    print("LOG: Starting routing node")
    # NOTE: All these are running on the assumption that the ports provided are integers lol
    NODE=Router() # Set global node variable to instance of Node
    NODE.set_address(RADDR_LIST[int(sys.argv[2])])
    NODE.set_neighbours(set_up_neighbours())
    print(f"LOG: Router running on port {PORT}")
    loop_listen()
