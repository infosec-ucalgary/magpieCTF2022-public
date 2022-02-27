import sys
import time
import socket
import threading

# RC2 encrypted with a key of n3tw0rk1ng
# and no IV on CyberChef
NOTE = "e7b67e867772b6f5868422df420bcb54dfee39665332664967c2cc33a3e51f0450f59744329e583c39cd86f1df93e9da069ce13bb8854effec4889c755e474914bfebb3ec7b45125ce8e5a7d3098385b901f725f6c91d0003994cb8a8fd6e60bc134a6306eb915794082df02798aa6f00eb24e58ff9707905d254143956e9cc0cb3cff030e5a8cbd4aabe324b2ec20742adebbc3f1fb00d4df73f1b4f862c7c2483d8177547e6ea60059498715e8fe279f613a86e52dcdebc045ddfde8b18952614e64736dbbb14b2173aa0763b16d8541cac32b5aa17e8434282551e54cf9529b046fb6b8f4b5b2d44a2d950184c3b0d2d60c338547317e1b7e212c92e0cf3ce9df727e39235e852bebfa5bb844491d991b88d1c714cdbd7875dfdc8b2dacc926c5ffc080517a6b3b9d9d55411b4b7a6f190a19835929caab044d647119a5a47e9afebf91d012312169ea9474d4554d4ed42ac582ce4ac12490636a6660872c5cd6075b747067be9fe22f1bbc448abfb1d0862b27bc843900d784860c214d923659f7674e2039c4148db3ea121197f4d786266c421d17330c64a9b97ac1f6ce7fe55898d2278206841ff44840749caeec0b39183d462f10aa0749b66c47a628d38f6cd24b49ab5effea698c98ea410f59b0ca74b98d3720c52bfe8bde079b968342a72b45e5c6475b939be6d15734404ebf640eacc1b62e39cddbb3fe6c0a991517f66774a8fb87635d2a79cf950fb216e6d3d997f341e8939f8b72d50a2d84a79ddb55d4d3cfc0aadec2405017c6710e0d6c7daac17fded01b519c66fc069ab7bfe32a55ae3aec40a89068b46de88f157a80a8948e540446d93a8127fd707564c6a6b0fdb6c96302f6dc4e4ae5a4e60b48af117b739dd9c7b9b6ed1fab11de39b305a828716c406b52cac5b4ab8aba53b0aa886edffb86d8616f46158ec5c1ef15f74e8e058f1e208a8283e566b445f104759bd50e42f0def5fa837b3901f6bb78522afc5a353836afe2079fb2b0cf6fc49ba457a092323c185c984138af3ea4087e8820e3f7191626fe346757061fbd588ee133f11f94c687801669716118f010500e9ee42e44093e084f289ec95985cd21630d73e0eba8233229a75412b982aeb459519a3a369b04e17dffebca38a29603b6cb196ff4afc13015b6fc195011c7c13e94550708f3a8e380959fa62a125ab84520219419b09cf73d660272bfd4b1692dc83e8508064e7f4d42590d10d081a3f865af65e0f7c712a57fa1e040cba7a625313729b05191f8d08b3b035b1e7c44ae1996641a156118cbab85d10f81ae0eeba6b37629179515edffd4a72d27407869d793df77b30cb89db847fa8f189ce8495ea9d8c4a5adf7c27e2c246fd2df6d6913bd2d34becba822197de6ea4324309d084cf4a404c5d99439bc7a29498d8de14a12a9f9d0b81b665568428be53aa2a011a608fc5f1b0e53bab7491e5969bf18168ec313afff723293a9ac1d918dd6f7456659ffcf542350338bb1d9ce0bfb418ff086c89dfeb585fccf1f51c617bdae06cf3f34dc521752a0909e6d0821dd18a39f8cf74305358afc25a804"
README = "TODO: Finish writing the readme for this and the encryption/decryption node"

def split_note(n):
    split_strings = [NOTE[i:i+n] for i in range(0, len(NOTE), n)]
    print(split_strings)
    return split_strings

class ClientThread(threading.Thread):
    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.didquit = False

    def run(self):
        try:
            while not self.didquit:
                self.send("\n---------MagpieNet Filesystem---------\n")
                self.send("- Current Files: note.txt, readme.txt\n")
                self.send("- Type HELP for options\n")
                self.send("> ")
                data = self.sock.recv(1024).decode('utf-8').strip()
                if len(data) > 0:
                    self.handle_msg(data)
            self.sock.close()
        except Exception as e:
            print(f"ERROR: {e}")
            self.sock.close()

    def send(self, msg):
        self.sock.send(msg.encode())

    def handle_msg(self, msg):
        global NOTE
        global README
        if msg == "HELP":
            self.send("\n------------HELP options------------\n")
            self.send("OPEN <filename> - Opens file with input name\n")
            self.send("QUIT - Close the filesystem\n")
        elif msg == "QUIT":
            self.send("\nGoodbye...\n")
            self.didquit = True
        elif msg == "OPEN note.txt":
            self.send("\n")
            self.send(NOTE)
            self.send("\n")
        elif msg == "OPEN readme.txt":
            self.send("\n")
            self.send(README)
            self.send("\n")

def handle_user_connections(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    while True:
        try:
            s.listen(1)
            csock, caddr = s.accept()
            csock.settimeout(30)
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
    msg = f"RENAME {address.split('.')[1]} fileserver"
    s.send(msg.encode())
    while True:
        time.sleep(0.01)
        # Just wait here
        pass
    s.close()

if __name__ == "__main__":
    threads = []
    tu = threading.Thread(target=handle_user_connections, args=[int(sys.argv[2])])
    tn = threading.Thread(target=handle_network_connection, args=["srv3.momandpopsflags.ca", int(sys.argv[1])])
    threads.append(tu)
    threads.append(tn)
    tu.start()
    tn.start()
    print("LOG: File nodes started, threads running...")
    for t in threads:
        t.join()
