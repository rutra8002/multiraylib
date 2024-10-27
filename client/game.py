import pyray as pr

class Game:
    def __init__(self, network):
        self.network = network
        self.player_pos = [100, 100]

    def start(self):
        pr.init_window(800, 600, "Client")
        pr.set_target_fps(60)

        receive_thread = self.network.start_threads()

        while not pr.window_should_close():
            self.handle_input()
            self.render()

        pr.close_window()
        self.network.client_socket.close()
        receive_thread.join()

    def handle_input(self):
        input_data = []
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            input_data.append("RIGHT")
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            input_data.append("LEFT")
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            input_data.append("UP")
        if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            input_data.append("DOWN")

        if input_data:
            self.network.send_data(f"{id(self.network.client_socket)},{','.join(input_data)}")

    def render(self):
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        for pos in self.network.players.values():
            pr.draw_rectangle(pos[0], pos[1], 50, 50, pr.BLUE)
        pr.end_drawing()