
import socket
import time
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((TCP_IP, TCP_PORT))
        self.socket.listen(1)
        self.client_list = []
        self.running = True
        print("setup server")

    def listen_for_clients(self):
        while self.running:
            conn, address = self.socket.accept()
            print('Connection address:', address)
            client_listen_thread = threading.Thread(target=self.listen_to_client, args=(conn,))
            self.client_list.append((conn, address, client_listen_thread))
            client_listen_thread.start()

    def listen_to_client(self, conn):
        while self.running:
            data_raw = conn.recv(BUFFER_SIZE)
            data = data_raw.decode()
            print("received data:", data)
            if data == "QUIT":
                for client in self.client_list:
                    if client[0] == conn:
                        self.client_list.remove(client)
                time.sleep(1)
                conn.send("GOODBYE".encode())
                return
            elif data == "SHUTDOWN":
                self.running = False
                return
            else:
                for client in self.client_list:
                    if client[0] != conn:
                        client[0].send(data_raw)

    def server_start(self):
        new_client_listen_thread = threading.Thread(target=srv.listen_for_clients)
        new_client_listen_thread.start()
        while True:
            time.sleep(3)
            if self.running is False:
                break
        new_client_listen_thread.join(1)
        for client in self.client_list:
            client[0].send("GOODBYE".encode())
            client[2].join(1)
        self.socket.close()


if __name__ == '__main__':
    srv = Server()
    srv.server_start()

