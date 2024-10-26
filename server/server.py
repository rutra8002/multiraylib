import socket
import threading
from server.client_handler import handle_client
from ui import ServerUI

class Server:
    def __init__(self, host='0.0.0.0', port=1234):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=handle_client, args=(client_socket, self.clients))
            client_handler.start()

if __name__ == "__main__":
    server = Server()
    ui = ServerUI(server)
    ui.run()