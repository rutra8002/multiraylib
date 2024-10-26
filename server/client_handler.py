def handle_client(client_socket, clients, server):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            for client in clients:
                if client != client_socket:
                    client.send(data)
            parts = data.decode('utf-8').split(',')
            if len(parts) == 3:
                player_id, x, y = parts
                server.players_positions[player_id] = (int(x), int(y))
        except:
            clients.remove(client_socket)
            client_socket.close()
            break