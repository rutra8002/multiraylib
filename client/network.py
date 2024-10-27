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
                    parts = data.split(',')
                    if len(parts) % 3 == 0:  # Ensure the data is in the expected format
                        self.players = {parts[i]: (int(parts[i+1]), int(parts[i+2])) for i in range(0, len(parts), 3)}
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