import socket
import threading
import subprocess

host = '127.0.0.1'
port = 8000

subprocess.Popen(["python", "home.py"])  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print("\n Received message:", message)
        except socket.error as e:
            print("\n Error receiving message:", str(e))
            break


receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

while True:
    message = input("Enter your message (or 'exit' to quit): ")
    client_socket.send(message.encode())
    if message == "exit":
        break

client_socket.close()
