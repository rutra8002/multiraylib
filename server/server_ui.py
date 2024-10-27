import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
from threading import Thread
from server import Server

class ServerUI(QMainWindow):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Server UI")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.players_tab = QWidget()
        self.logs_tab = QWidget()
        self.info_tab = QWidget()
        self.inputs_tab = QWidget()

        self.tabs.addTab(self.players_tab, "Players")
        self.tabs.addTab(self.logs_tab, "Logs")
        self.tabs.addTab(self.info_tab, "Server Info")
        self.tabs.addTab(self.inputs_tab, "Player Inputs")

        self.init_players_tab()
        self.init_logs_tab()
        self.init_info_tab()
        self.init_inputs_tab()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(10)

    def init_players_tab(self):
        layout = QVBoxLayout()
        self.players_info = QTextEdit()
        self.players_info.setReadOnly(True)
        layout.addWidget(self.players_info)
        self.players_tab.setLayout(layout)

    def init_logs_tab(self):
        layout = QVBoxLayout()
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        layout.addWidget(self.logs)
        self.logs_tab.setLayout(layout)

    def init_info_tab(self):
        layout = QVBoxLayout()
        self.server_info = QLabel()
        layout.addWidget(self.server_info)
        self.info_tab.setLayout(layout)

    def init_inputs_tab(self):
        layout = QVBoxLayout()
        self.inputs_info = QTextEdit()
        self.inputs_info.setReadOnly(True)
        layout.addWidget(self.inputs_info)
        self.inputs_tab.setLayout(layout)

    def update_ui(self):
        self.update_players_info()
        self.update_logs()
        self.update_server_info()
        self.update_inputs_info()

    def update_players_info(self):
        players_text = "Players Positions:\n"
        for player_id, pos in self.server.get_players_positions().items():
            players_text += f"Player {player_id}: {pos}\n"
        self.players_info.setText(players_text)

    def update_logs(self):
        self.logs.setText(self.server.get_logs())

    def update_server_info(self):
        self.server_info.setText(f"Host: {self.server.host}\nPort: {self.server.port}")

    def update_inputs_info(self):
        inputs_text = "Player Inputs:\n"
        for player_id, inputs in self.server.get_players_inputs().items():
            inputs_text += f"Player {player_id}: {inputs}\n"
        self.inputs_info.setText(inputs_text)

    def run(self):
        self.show()
        server_thread = Thread(target=self.server.start)
        server_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = Server()
    ui = ServerUI(server)
    ui.run()
    sys.exit(app.exec())