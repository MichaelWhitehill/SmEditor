import socket
from threading import Thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


class JsonController:
    def __init__(self, editor):
        self.sm_editor = editor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))
        self.send_message("First message")
        self.exit = False

    def send_message(self, message):
        self.socket.send(message.encode())

    def listen(self):
        while True:
            in_message = self.socket.recv(BUFFER_SIZE)
            in_message = in_message.decode()
            print(str(in_message))
            if in_message == "GOODBYE":
                self.exit = True
                return

    def close(self):
        self.socket.close()

