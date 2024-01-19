import socket
from bs4 import BeautifulSoup

host = "localhost"
port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
client.send(bytes("GET / HTTP1.1\nHost: localhost\n\n"))

response = client.recv(4096)

print(response)