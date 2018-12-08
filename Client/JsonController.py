import socket
from threading import Thread
import json

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

    def propagate_insert(self, index, insert_text):
        fields = {"op": "insert", "index": str(index), "insert_text": str(insert_text)}
        json_fields = json.dumps(fields)
        json_string = str(json_fields)
        self.send_message(json_string)

    def propagate_delete(self, index1, index2):
        fields = {"op": "delete", "index1": str(index1), "index2": str(index2)}
        json_fields = json.dumps(fields)
        json_string = str(json_fields)
        self.send_message(json_string)

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

