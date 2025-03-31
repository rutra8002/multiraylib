import socket
import threading

def handle_client(client_socket, server):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            parts = data.decode('utf-8').split(',')
            player_id = parts[0]
            inputs = parts[1:]
            server.update_player_position(player_id, inputs)
        except:
            server.clients.remove(client_socket)
            client_socket.close()
            break

class Server:
    def __init__(self, host='0.0.0.0', port=1234):
        self.host = host
        self.port = port
        self.clients = []
        self.players_positions = {}
        self.players_inputs = {}
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

    def get_players_inputs(self):
        return self.players_inputs

    def get_logs(self):
        return "\n".join(self.logs)

    def update_player_position(self, player_id, inputs):
        if player_id not in self.players_positions:
            self.players_positions[player_id] = [100, 100]

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
        self.players_inputs[player_id] = inputs
        self.broadcast_positions()

    def broadcast_positions(self):
        positions = ",".join([f"{pid},{pos[0]},{pos[1]}" for pid, pos in self.players_positions.items()])
        for client in self.clients:
            try:
                client.send(positions.encode('utf-8'))
            except:
                self.clients.remove(client)
                client.close()

if __name__ == "__main__":
    server = Server()
    server.start()