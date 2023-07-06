import socket
import threading

host = '127.0.0.1'
port = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(10)
print("Server listening on", host, "port", port)

clients = {}

id = 1
prev = 0

def handle_client(client_socket, client_address, group):
    while True:
        message = client_socket.recv(1024).decode()
        if message == "exit":
            break
        print(f"Group {group}, Client {client_address}: {message}")

        for socket_item, address_item in clients[group]:
            if socket_item != client_socket:
                socket_item.send(message.encode())

    clients[group].remove((client_socket, client_address))
    print(f"Client {client_address} left Group {group}")

    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    print("Connected with client", client_address)

    # generate number group
    group = len(clients) + 1
    if id == 1:
        id = 2
        prev = group
    else:
        id = 1
        group = prev
    print(f"len(clients) = {len(clients)}")

    # input ke group nya
    # print(f"{clients}")
    if group not in clients:
        clients[group] = []

    print(f"Client {client_address} joined Group {group}")

    clients[group].append((client_socket, client_address))

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, group))
    client_thread.start()
