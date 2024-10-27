from network import Network
from game import Game
from server_input_window import ServerInputWindow

if __name__ == "__main__":
    input_window = ServerInputWindow()
    server_ip, server_port = input_window.start()
    network = Network(server_ip, server_port)
    game = Game(network)
    game.start()