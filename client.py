import socket

PORT = 5050
SERVER = "212.71.239.132"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_SIZE = 1024

def connect():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def start():
    answer = input("Connect? (y/n)")
    if answer.lower() != "y":
        return

    connection = connect()
    
    while True:
        msg = input("Message (q for quit): ")
        if msg == "q":
            break
        
        send(connection, msg)
    
    send(connection, DISCONNECT_MESSAGE)

start()