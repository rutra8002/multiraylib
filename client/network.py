import socket
import threading

class Network:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self.players = {}

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    # Split by comma and process the data in triplets
                    parts = data.split(',')
                    temp_players = {}

                    # Process data in chunks of 3 (player_id, x, y)
                    for i in range(0, len(parts), 3):
                        if i + 2 < len(parts):  # Make sure we have all 3 elements
                            try:
                                player_id = parts[i]
                                x = int(parts[i + 1])
                                y = int(parts[i + 2])
                                temp_players[player_id] = (x, y)
                            except (ValueError, IndexError):
                                pass  # Skip invalid data

                    if temp_players:
                        self.players = temp_players
                    else:
                        print(f"Unexpected data format: {data}")
            except OSError:
                break

    def send_data(self, data):
        try:
            self.client_socket.send(data.encode('utf-8'))
        except OSError:
            pass

    def start_threads(self):
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()
        return receive_thread