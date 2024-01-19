import socket
import json
import threading
import os
import re

HOST = '127.0.0.1'
PORT = 12346

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.connect((HOST, PORT))

print(f"Connected to {HOST}:{PORT}")

class ReceiveState:
    def __init__(self):
        self.receivefree = 1
        self.upload_permission = 0
        self.upload_free = 1
        self.reason = ''
        self.download_file_found = 0
        self.download_free = 1
        self.file_size = 0

fs = ReceiveState()

def receive_message():
    while True:
        if fs.receivefree:
            message = server_socket.recv(1024).decode('utf-8')
            print(message)
            struct = json.loads(message)
            _type = struct["type"]
            if _type == "message":
                print(struct["message"])
            if _type == "upload not permitted":
                fs.upload_permission = 0
                fs.reason = struct["reason"]
                fs.upload_free = 1
            if _type == "upload permitted":
                fs.upload_permission = 1
                fs.upload_free = 1
            if _type == "file not found":
                fs.download_file_found = 0
                fs.download_free = 1
            if _type == "file found":
                fs.download_file_found = 1
                fs.download_free = 1
                fs.receivefree = 0
                fs.file_size = struct["file size"]

receive_message = threading.Thread(target=receive_message)
receive_message.daemon = True
receive_message.start()

nickname = input("Input your nickname: ")
roomname = input("Input the room you want to enter (Enter for General): ")
if roomname == '':
    roomname = 'General'
    
struct = {
    "type" : "connect",
    "name" : nickname,
    "room" : roomname
}
message = json.dumps(struct).encode('utf-8')
server_socket.send(message)


while True:
    input_message = input()
    x = re.search('^upload: .*', input_message)
    if x != None:
        message = input_message
        file_path = message[8 : (x.span()[1])]
        if os.path.isfile(file_path):
            struct = {
                "type" : "upload file",
                "file name" : os.path.basename(file_path),
                "file size" : os.path.getsize(file_path)
            }
            message = json.dumps(struct).encode('utf-8')
            server_socket.send(message)
            fs.upload_free = 0
            while not fs.upload_free:
                pass
            if not fs.upload_permission:
                print(f"Failed: {type}\nReason: {fs.reason}")
            else:
                f = open(file_path, "rb")
                file_content = f.read()
                server_socket.send(file_content)
                f.close()
        else:
            print("The path to this file cannot be found\n")
    x = re.search('^download: .*', input_message)
    if x != None:
        message = input_message
        file_name = message[10 : (x.span()[1])]
        struct = {
            "type" : "download file",
            "file name" : file_name
        }
        fs.download_free = 0
        message = json.dumps(struct).encode('utf-8')
        server_socket.send(message)
        while not fs.download_free:
            pass
        if not fs.download_file_found:
            print(f"Failed: File not found")
        else:
            file_size = fs.file_size
            decision = input(f"Download file {file_name} , size: {file_size}. Press (Y/n) to confirm")
            if decision == '' or decision == 'Y' or decision == 'y':
                struct = {
                    "type" : "download confirm"
                }
                response_message = json.dumps(struct).encode('utf-8')
                server_socket.send(response_message)
                file_content = server_socket.recv(file_size)
                f = open(file_name, "wb")
                f.write(file_content)
                f.close()
            else:
                struct = {
                    "type" : "download abort"
                }
                response_message = json.dumps(struct).encode('utf-8')
                server_socket.send(response_message)
                print("File not found on the server media")
        fs.receivefree = 1
    elif message == 'exit':
        break
    else:
        message = input_message
        struct = {
            "type" : "message",
            "message" : message
        }
        message = json.dumps(struct).encode('utf-8')
        server_socket.send(message)
    
server_socket.close()