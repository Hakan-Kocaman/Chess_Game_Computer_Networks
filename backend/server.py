import socket
import threading
import pickle
import sys

ip = "127.0.0.1"
port = 5432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))

client_socket = None

services = {
    "move": move_service,
    "chat": chat_service,
}

def handle_client():
    global client_socket
    server_socket.listen()
    while True:
            client_socket, addr = server_socket.accept()
            data = client_socket.recv(1024)
            request = pickle.loads(data)
            thrd=threading.Thread(target=controller_handler, args=(client_socket, addr, request))
            thrd.start()

def controller_handler(client_socket, addr, request):
    if client_socket:
        try:
            requested_service = services.get(request["service"])
            if requested_service:
                response = requested_service(request)
                client_socket.send(pickle.dumps(response))
            else:
                client_socket.send(pickle.dumps({"error": "unknown service"}))
                
            client_socket.close()

        except Exception as e:
                print(f"Error receiving data from client: {e}")
                client_socket.close()
                client_socket = None
                print(f"Client disconnected {addr}")

def move_service(command):
    if client_socket:
        try:
            data = command["command"]
            return data
        except Exception as e:
            print(f"Error sending command to client: {e}")
    else:
        print("Client is not connected.")

def chat_service(message):
    if client_socket:
        try:
            data = message["message"]
            return data
        except Exception as e:
            print(f"Error sending message to client: {e}")
    else:
        print("Client is not connected.")


if __name__ == "__main__":
    print("Starting server...")
    controller_thread = threading.Thread(target=controller_handler)
    controller_thread.start()
    controller_thread.join()
    print("Server shutting down.")