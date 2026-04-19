import threading
import pickle
import socket_manager

# request= {
#     "URL": determines the service,
#     "body": {} request data
# }

server_socket = socket_manager.server_socket

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

def move_service(request_body):
    try:
        data = request_body
        return data
    except Exception as e:
         print(f"Error sending command to client: {e}")

def chat_service(request_body):
    try:
        data = request_body["message"]
        return data
    except Exception as e:
            print(f"Error sending message to client: {e}")

services = {
    "move": move_service,
    "chat": chat_service,
}

def handle_client():
    socket_manager.listen()
    while True:
            client_socket, addr = socket_manager.accept()
            data = client_socket.recv(1024)
            request = pickle.loads(data)
            thrd=threading.Thread(target=controller_handler, args=(client_socket, addr, request))
            thrd.start()



