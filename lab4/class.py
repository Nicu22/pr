import socket

HOST = '127.0.0.1'
PORT = 8000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))


server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

def get_product_info(product):
    return f"""
    <h1>Course Name: {product["name"]}<br></h1>
    <div>Author: {product["author"]}<br><br></div>
    <div>Price: {product["price"]} EURO<br><br></div>
    <div>Description: {product["description"]}<br><br></div>
    """

def is_it_product(path):
    if path[0:9] == '/products':
        try:
            inte = int(path[10:])
        except:
            return 100
        return int(path[10:])
    return 100

products = [
  {
    "name" : "Fluent Python: Clear, Concise, and Effective Programming",
    "author" : "Luciano Ramalho",
    "price" : 39.95,
    "description" : "Don't waste time bending Python to fit patterns you've learned in other languages. Python's simplicity lets you become productive quickly, but often this means you aren't using everything the language has to offer. With the updated edition of this hands-on guide, you'll learn how to write effective, modern Python 3 code by leveraging its best ideas. "
  },
  {
    "name" : "Introducing Python: Modern Computing in Simple Packages",
    "author" : "Bill Lubanovic",
    "price" : 27.49,
    "description" : "Easy to understand and fun to read, this updated edition of Introducing Python is ideal for beginning programmers as well as those new to the language. Author Bill Lubanovic takes you from the basics to more involved and varied topics, mixing tutorials with cookbook-style code recipes to explain concepts in Python 3. End-of-chapter exercises help you practice what you've learned."
  }
]

while True:
    
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")  
    
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}") 
    
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]

    if path == '/':
        response_content = \
        f"""
        <a href="/home">Go to home boi</a>
        """
    elif path == '/home':
        response_content = \
        f"""
        <h1>Product Home</h1>
        <div>
        <a href="/products">Products</a>
        </div>
        <div>
        <a href="/aboutus">About Us</a>
        </div>
        <div>
        <a href="/contacts">Contacts</a>
        </div>
        """
    elif path == '/aboutus':
        response_content = '<div>We are the aboutus</div><a href="/home">Go back</a>'
    elif path == '/contacts':
        response_content = '<div>Contacts:</div><div>\n555-6969</div><a href="/home">Go back</a>'
    elif path == '/products':
        response_content = \
        f"""
        <h1>PRODUCTS!!!!</h1>
        <div>
            <a>Product {1}:</a>
            <a href="/products/0">{products[0]["name"]}</a>
        </div>
        <div>
            <a>Product {2}:</a>
            <a href="/products/1">{products[1]["name"]}</a>
        </div>
        <a href="/home">Go back</a>
            """
    elif is_it_product(path) < 2:
        response_content = get_product_info(products[is_it_product(path)]) + """<a href="/products">Go back</a>"""
    else:
        response_content = None

    if response_content != None:
        response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response_content}'
    else:
        response = 'HTTP/1.1 404\nContent-Type: text/html\n\n<h1>Error Code 404</h1>'
    client_socket.send(response.encode('utf-8'))

    client_socket.close()