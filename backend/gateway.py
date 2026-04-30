import threading
import pickle
import socket_manager
import controllers
from dtos.requests import request


# request= {
#     "URL": determines the service,
#     "from": player color, 
#     .....
# }

server_socket = socket_manager.server_socket

controller_list = {
   "chat": controllers.chat_controller,
   "get_possible_moves": controllers.get_possible_moves_controller,
   "move": controllers.move_controller
}

def controller_handler(client_socket, addr, request):
    if client_socket:
        try:
            requested_controller = controller_list.get(request.URL)
            if requested_controller:
                response = requested_controller(request) 
                if not response:
                     print(f"Controller {request.URL} returned an error.")       
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
        request = request(
            URL=request.get("URL"),
            sender=request.get("from"),
            body=request.get("body")
        )
        controller_thread=threading.Thread(target=controller_handler, args=(client_socket, request))
        controller_thread.start()








