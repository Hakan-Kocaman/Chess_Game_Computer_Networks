import threading
import pickle
import socket_manager
import services

# request= {
#     "URL": determines the service,
#     "body": {} request data
# }

server_socket = socket_manager.server_socket

services = {
    "move": services.move_service,
    "chat": services.chat_service,
}

def controller_handler(client_socket, addr, request):
    if client_socket:
        try:
            requested_service = services.get(request["URL"])
            if requested_service:
                response = requested_service(request["body"])
                client_socket.send(pickle.dumps(response))
            else:
                client_socket.send(pickle.dumps({"error": "unknown service"}))
                
            client_socket.close()

        except Exception as e:
                print(f"Error receiving data from client: {e}")
                client_socket.close()
                client_socket = None
                print(f"Client disconnected {addr}")

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        request = pickle.loads(data)
        controller_thread=threading.Thread(target=controller_handler, args=(client_socket, request))
        controller_thread.start()








