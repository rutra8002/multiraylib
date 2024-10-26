import socket
import threading
from client_handler import handle_client

class Server:
    def __init__(self, host='0.0.0.0', port=1234):
        self.host = host
        self.port = port
        self.clients = []
        self.players_positions = {}
        self.logs = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.log(f"Server started on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.log(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=handle_client, args=(client_socket, self.clients, self))
            client_handler.start()

    def log(self, message):
        self.logs.append(message)
        print(message)

    def get_players_positions(self):
        return self.players_positions

    def get_logs(self):
        return "\n".join(self.logs)