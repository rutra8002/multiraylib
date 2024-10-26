def handle_client(client_socket, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            for client in clients:
                if client != client_socket:
                    client.send(data)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break