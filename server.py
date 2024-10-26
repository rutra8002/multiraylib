import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=1234):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                for client in self.clients:
                    if client != client_socket:
                        client.send(data)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = Server()
    server.start()