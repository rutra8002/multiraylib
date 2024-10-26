import socket
import threading
import pyray as pr

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self.player_pos = [100, 100]
        self.players = {}

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    parts = data.split(',')
                    if len(parts) == 3:
                        player_id, x, y = parts
                        self.players[player_id] = (int(x), int(y))
                    else:
                        print(f"Unexpected data format: {data}")
            except OSError:
                break

    def send_data(self):
        while True:
            try:
                data = f"{id(self.client_socket)},{self.player_pos[0]},{self.player_pos[1]}"
                self.client_socket.send(data.encode('utf-8'))
                pr.wait_time(0.01)
            except OSError:
                break

    def start(self):
        pr.init_window(800, 600, "Client")
        pr.set_target_fps(60)

        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_data)
        send_thread.start()

        while not pr.window_should_close():
            if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
                self.player_pos[0] += 5
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
                self.player_pos[0] -= 5
            if pr.is_key_down(pr.KeyboardKey.KEY_UP):
                self.player_pos[1] -= 5
            if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
                self.player_pos[1] += 5

            pr.begin_drawing()
            pr.clear_background(pr.RAYWHITE)
            pr.draw_rectangle(self.player_pos[0], self.player_pos[1], 50, 50, pr.RED)
            for pos in self.players.values():
                pr.draw_rectangle(pos[0], pos[1], 50, 50, pr.BLUE)
            pr.end_drawing()

        pr.close_window()
        self.client_socket.close()
        receive_thread.join()
        send_thread.join()

if __name__ == "__main__":
    server_ip = input("Enter server IP (localhost for localhost): ")
    server_port = int(input("Enter server port: "))
    client = Client(server_ip, server_port)
    client.start()