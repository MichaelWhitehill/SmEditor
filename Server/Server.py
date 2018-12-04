
import socket
import json
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    data = data.decode()
    print("recieved data:", data)
    if data == "QUIT":
        time.sleep(1)
        conn.send("GOODBYE".encode())
        break
conn.close()

