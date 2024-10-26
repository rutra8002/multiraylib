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
            self.network.send_data(f"{id(self.network.client_socket)},{self.player_pos[0]},{self.player_pos[1]}")
            self.render()

        pr.close_window()
        self.network.client_socket.close()
        receive_thread.join()

    def handle_input(self):
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.player_pos[0] += 5
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.player_pos[0] -= 5
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.player_pos[1] -= 5
        if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.player_pos[1] += 5

    def render(self):
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_rectangle(self.player_pos[0], self.player_pos[1], 50, 50, pr.RED)
        for pos in self.network.players.values():
            pr.draw_rectangle(pos[0], pos[1], 50, 50, pr.BLUE)
        pr.end_drawing()