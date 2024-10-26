import tkinter as tk
from threading import Thread

class ServerUI:
    def __init__(self, server):
        self.server = server
        self.root = tk.Tk()
        self.root.title("Server UI")
        self.log = tk.Text(self.root, state='disabled', width=80, height=20)
        self.log.pack()

    def run(self):
        self.update_log("Server started.")
        server_thread = Thread(target=self.server.start)
        server_thread.start()
        self.root.mainloop()

    def update_log(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')