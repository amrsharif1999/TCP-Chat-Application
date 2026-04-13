import socket
import threading

HOST = "127.0.0.1"
PORT = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message, sender=None):
    for client in clients[:]:
        if client != sender:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        name = usernames[index]
        clients.remove(client)
        usernames.remove(name)
        client.close()
        broadcast(f"{name} left the chat.".encode())

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            broadcast(message, client)
        except:
            remove_client(client)
            break

print(f"Server is running on {HOST}:{PORT}")

while True:
    client, address = server.accept()
    print("Connected:", address)

    client.send("NAME".encode())
    username = client.recv(1024).decode().strip()

    clients.append(client)
    usernames.append(username)

    print(username, "joined")
    broadcast(f"{username} joined the chat.".encode())

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.daemon = True
    thread.start()