from network import Network
from game import Game

if __name__ == "__main__":
    server_ip = input("Enter server IP (localhost for localhost): ")
    server_port = int(input("Enter server port: "))
    network = Network(server_ip, server_port)
    game = Game(network)
    game.start()