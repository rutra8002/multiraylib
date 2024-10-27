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
            client_handler = threading.Thread(target=handle_client, args=(client_socket, self))
            client_handler.start()

    def log(self, message):
        self.logs.append(message)
        print(message)

    def get_players_positions(self):
        return self.players_positions

    def get_logs(self):
        return "\n".join(self.logs)

    def update_player_position(self, player_id, inputs):
        if player_id not in self.players_positions:
            self.players_positions[player_id] = [100, 100]  # Default position

        x, y = self.players_positions[player_id]
        for input in inputs:
            if input == "RIGHT":
                x += 5
            elif input == "LEFT":
                x -= 5
            elif input == "UP":
                y -= 5
            elif input == "DOWN":
                y += 5

        self.players_positions[player_id] = (x, y)
        self.broadcast_positions()

    def broadcast_positions(self):
        positions = ",".join([f"{pid},{pos[0]},{pos[1]}" for pid, pos in self.players_positions.items()])
        for client in self.clients:
            try:
                client.send(positions.encode('utf-8'))
            except:
                self.clients.remove(client)
                client.close()