import socket
import regex as reg

product_data = [
    {
        "id": 1,
        "name": "Mr Mercedes",
        "author": "Stephen King",
        "description": "Tells the story of a psychopathic killer who drives a stolen Mercedes into a crowd and a recently retired detective who tries to bring him down.  "
    },
    {
        "id": 2,
        "name": "1884 - Nineteen Eighty-Four Novel by George Orwell",
        "author": "George Orwel",
        "description": "Nineteen Eighty-Four is a dystopian social science fiction novel and cautionary tale by English writer George Orwell. It was published on 8 June 1949 by Secker & Warburg as Orwell's ninth and final book completed in his lifetime."
    }
]

HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    print(request_line)
    path = request_line[1]

    response_content = ''
    status_code = 200

    if path == '/':
        with open('html_content/welcome.html') as home_page:
            response_content = home_page.read()

    elif path == '/about':
        with open('html_content/about.html') as about_page:
            response_content = about_page.read()
    elif path == '/home':
        with open('html_content/home.html') as home_page:
            response_content = home_page.read()
    elif path == '/products':
        with open('html_content/products.html') as products_page:
            response_content = products_page.read()
        for product in product_data:
            response_content += f"<a href='/product/{product['id']}'> Product: {product['name']} </a><br>"
    elif reg.match(r"/product/[0-9]+", path):
        product_id = int(reg.split(r"/", path)[2])

        for product in product_data:
            if product['id'] == product_id:
                response_content = f"""
                <h2>Product review</h2>
                <ul>
                        <li>
                            <span>Product ID: </span>
                            <span>{product['id']}</span>
                        </li>
                        <li>
                            <span>Product name: </span>
                            <span>{product['name']}</span>
                        </li>
                        <li>
                            <span>Product author: </span>
                            <span>{product['author']}</span>
                        </li>
                        <li>
                            <span>Product description: </span>
                            <span>{product['description']}</span>
                        </li>   
                                          
                </ul>
                """

    else:
        with open('html_content/not_found.html') as products_page:
            response_content = products_page.read()

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        handle_request(client_socket)
    except KeyboardInterrupt:
        pass