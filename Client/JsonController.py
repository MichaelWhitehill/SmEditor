import socket
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
OP = "op"
INSERT = "insert"
DELETE = "delete"
INDEX1 = "index1"
INDEX2 = "index2"
INSERT_TEXT = "insert_text"


class JsonController:
    def __init__(self, editor):
        self.sm_editor = editor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))
        self.exit = False

    def send_message(self, message):
        self.socket.send(message.encode())

    def propagate_insert(self, index, insert_text):
        fields = {OP: INSERT, INDEX1: str(index), INSERT_TEXT: str(insert_text)}
        json_fields = json.dumps(fields)
        json_string = str(json_fields)
        self.send_message(json_string)

    def propagate_delete(self, index1, index2):
        fields = {OP: DELETE, INDEX1: str(index1), INDEX2: str(index2)}
        json_fields = json.dumps(fields)
        json_string = str(json_fields)
        self.send_message(json_string)

    def listen(self):
        while True:
            in_message = self.socket.recv(BUFFER_SIZE)
            in_message = in_message.decode()
            print("RECEIVED{" + str(in_message) + "}")
            if in_message == "GOODBYE":
                self.exit = True
                return
            else:
                data = json.loads(in_message)
                from Client.SmEditor import Cursor
                if data[OP] == INSERT:
                    insert_cursor = Cursor(data[INDEX1])
                    self.sm_editor.net_insert(insert_cursor, data[INSERT_TEXT])
                if data[OP] == DELETE:
                    c1 = Cursor(data[INDEX1])
                    c2 = Cursor(data[INDEX2])
                    self.sm_editor.net_delete(c1, c2)

    def close(self):
        self.socket.close()

