import threading
import socket

PORT = 5050
SERVER = "212.71.239.132"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_SIZE = 1024

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def start():
    print("[SERVER STARTED]")
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    connected = True
    try:
        while connected:
            msg = conn.recv(MSG_SIZE).decode(FORMAT)
            if not msg:
                break
            
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

            with clients_lock:
                for c in clients:
                    try:
                        c.sendall(f"[{addr}] {msg}".encode(FORMAT))
                    except ConnectionResetError:
                        pass

    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()

start()