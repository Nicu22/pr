import socket
import threading
import json
import os

EIGHT_MEGABYTES = 8388608

HOST = '127.0.0.1'
PORT = 12346

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print("Server is listening to 127.0.0.1:12345")

client_rooms = dict()

def send_all(clients : list[socket.socket], buffer, exception=None):
    print(buffer)
    for client in clients:
        if client != exception:
            client.send(buffer)

def handle_client(client_socket : socket, client_address):
    name = ''
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(f"{client_socket}\n{message}")
        struct = json.loads(message)
        _type = struct["type"]

        if not message:
            break
        elif _type == "connect":
            name = struct["name"]
            room = struct["room"]
            if room in client_rooms.keys():
                client_rooms[room].append(client_socket)
                struct = {
                    "type" : "message",
                    "message" : f"{name} has joined the room"
                }
                response_message = json.dumps(struct)
                send_all(client_rooms[room], response_message.encode('utf-8'), exception=client_socket)
            else:
                client_rooms[room] = [client_socket]

        elif _type == "message":
            message = struct["message"]
            struct = {
                "type" : "message",
                "message" : f"{name}: {message}"
            }
            message = json.dumps(struct).encode('utf-8')
            send_all(client_rooms[room], message, exception=client_socket)
            
        elif _type == "upload file":
            print("uploadddd")
            file_name = struct["file name"]
            file_size = struct["file size"]
            if file_size > EIGHT_MEGABYTES:
                struct = {
                    "type" : "upload not permitted",
                    "reason" : "File too big, can't send files bigger than 8 MB"
                }
                response_message = json.dumps(struct).encode('utf-8')
                client_socket.send(response_message)
            elif file_name in os.listdir("./SERVER_MEDIA"):
                struct = {
                    "type" : "upload not permitter",
                    "reason" : "File with the same name already exists in server media"
                }
                response_message = json.dumps(struct).encode('utf-8')
                client_socket.send(response_message)
            else:
                struct = {
                    "type" : "upload permitted"
                }
                response_message = json.dumps(struct).encode('utf-8')
                client_socket.send(response_message)
                print("permission sent")
                f = open(f"./SERVER_MEDIA/{file_name}", "wb")
                file_content = client_socket.recv(file_size)
                print(file_content)
                f.write(file_content)
                f.close()
                struct = {
                    "type" : "message",
                    "message" : f"{name} has uploaded {file_name}, {file_size} bytes"
                }
                response_message = json.dumps(struct).encode('utf-8')
                send_all(client_rooms[room], response_message)
            
        elif _type == "download file":
            file_name = struct["file name"]
            file_path = f"./SERVER_MEDIA/{file_name}"
            files = os.listdir("./SERVER_MEDIA")
            if file_name in files:
                file_size = os.path.getsize(file_path)
                struct = {
                    "type" : "file found",
                    "file size" : file_size
                }
                response_message = json.dumps(struct).encode('utf-8')
                client_socket.send(response_message)
                print("file found")
                message = client_socket.recv(1024).decode('utf-8')
                struct = json.loads(message)
                type = struct["type"]
                print(type)
                if type == "download confirm":
                    f = open(file_path, "rb")
                    file_content = f.read()
                    client_socket.send(file_content)
                    f.close()
                elif type == "download abort":
                    pass
            else:
                struct = {
                    "type" : "file not found"
                }
                response_message = json.dumps(struct).encode('utf-8')
                client_socket.send(response_message)
                pass
    client_rooms[room].remove(client_socket)
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"{client_socket} connected.")
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()