def handle_client(client_socket, server):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            parts = data.decode('utf-8').split(',')
            player_id = parts[0]
            inputs = parts[1:]
            server.update_player_position(player_id, inputs)
        except:
            server.clients.remove(client_socket)
            client_socket.close()
            break