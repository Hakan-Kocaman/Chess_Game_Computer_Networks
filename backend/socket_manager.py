import socket

HOST_IP = "0.0.0.0"
HOST_PORT = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

print(f"[LISTENING] Chess server {HOST_IP}:{HOST_PORT} listening...")