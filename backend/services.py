
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
