import socket
import json
from routing import do_routing
from tinydb import TinyDB, Query
import requests



query = Query()

max_followers = 2
class Service:
    def __init__(self, service_info, dbfile):
        self.service_info = service_info
        self.udp_host = "127.0.0.1"
        self.udp_port = 8000
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dbfile = dbfile
        try:
            self.udp_socket.bind((self.udp_host, self.udp_port))
            print("socket binded")
            self.role = "leader"

            self.followers = []
            curr_followers = 0

            while True:

                data, address = self.udp_socket.recvfrom(1024)

                message = json.loads(data.decode('utf-8'))

                if message["type"] == "accepted":

                    self.udp_socket.sendto(str.encode(json.dumps(self.service_info)), address)

                elif message["type"] == "follower info":
                    
                    self.followers.append(message["payload"])
                    print("follower added")
                    curr_followers += 1

                if curr_followers == max_followers:
                    break

        except:
            
            self.role = "follower"
            self.udp_socket.sendto(
                json.dumps({
                    "type" : "accepted"
                }).encode('utf-8'),
                (self.udp_host, self.udp_port)
            )
            self.leader_data = json.loads(self.udp_socket.recvfrom(1024)[0].decode('utf-8'))
            self.udp_socket.sendto(
                json.dumps({
                    "type" : "follower info",
                    "payload" : self.service_info
                }).encode('utf-8'),
                (self.udp_host, self.udp_port)
            )

    def start_http(self):
        do_routing(self)
        self.app.run(
            self.service_info["host"],
            self.service_info["port"]
            )
        print("HTTP Server started")
        
    def init_database(self):
        self.db = TinyDB(self.dbfile)

    def create_product(self, request):
        try:
            print("request", request.get_json())
        except Exception as e:
            print(e)
        if self.role == "leader":

            product_info = request.json
            try:
                if not self.db.contains(query.id == product_info["id"]):
                    self.db.insert(product_info)
                    for follower in self.followers:
                        requests.post(
                            f"http://{follower['host']}:{follower['port']}/product",
                            json = product_info,
                            headers = {"Token" : "Leader"}
                            )
                    return {
                        "message" : "Product Creation Succesful"
                    }, 200
                else:
                    return {
                        "message" : "Product with this ID already exists"
                    }, 400
            except KeyError:
                return {
                    "message" : "Bad request"
                }, 400
            except:
                return {
                    "message" : "Something happened in the server"
                }, 500

        elif self.role == "follower":
            product_info = request.json
            headers = request.headers
            try:
                if headers["Token"] == "Leader":
                    self.db.insert(product_info)
                    return {
                        "message" : "Product Creation Succesful"
                    }, 200
                else:
                    return {
                        "message" : "Access Denied"
                    }, 403
            except:
                return {
                    "message" : "Access Denied"
                }, 403

    def update_product(self, request):
        if self.role == "leader":
            product_info = request.json
            try:
                if self.db.contains(query.id == product_info["id"]):
                    self.db.update(product_info, query.id == product_info["id"])
                    for follower in self.followers:
                        requests.put(
                            f"http://{follower['host']}:{follower['port']}/product",
                            json = product_info,
                            headers = {"Token" : "Leader"}
                            )
                    return {
                        "message" : "Product Update Succesful"
                    }, 200
                else:
                    return {
                        "message" : "This Product Does Not Exist"
                    }, 400
            except KeyError:
                return {
                    "message" : "Bad request"
                }, 400
            except:
                return {
                    "message" : "Something happened in the server"
                }, 500

        elif self.role == "follower":
            print("received")
            product_info = request.json
            headers = request.headers
            try:
                if headers["Token"] == "Leader":
                    self.db.update(product_info, query.id == product_info["id"])
                    return {
                        "message" : "Product Update Succesful"
                    }, 200
                else:
                    return {
                        "message" : "Access Denied"
                    }, 403
            except:
                return {
                    "message" : "Access Denied"
                }, 403

    def delete_product(self, request):
        if self.role == "leader":
            product_info = request.json
            try:
                if self.db.contains(query.id == product_info["id"]):
                    self.db.remove(query.id == product_info["id"])
                    for follower in self.followers:
                        requests.delete(
                            f"http://{follower['host']}:{follower['port']}/product",
                            json = product_info,
                            headers = {"Token" : "Leader"}
                            )
                    return {
                        "message" : "Product Deletion Succesful"
                    }, 200
                else:
                    return {
                        "message" : "This Product Does Not Exist"
                    }, 400
            except KeyError:
                return {
                    "message" : "Bad request"
                }, 400
            except:
                return {
                    "message" : "Something happened in the server"
                }, 500

        elif self.role == "follower":
            product_info = request.json
            headers = request.headers
            try:
                if headers["Token"] == "Leader":
                    self.db.remove(query.id == product_info["id"])
                    return {
                        "message" : "Product Deletion Succesful"
                    }, 200
                else:
                    return {
                        "message" : "Access Denied"
                    }, 403
            except:
                return {
                    "message" : "Access Denied"
                }, 403

    def read_product(self, request):
        try:
            product_info = request.json
            print(product_info)
            if self.db.contains(query.id == product_info["id"]):
                return self.db.search(query.id == product_info["id"]), 200
            else:
                return {
                    "message" : "This Product Does Not Exist"
                }, 400
        except:
            return {
                "message" : "Bad request"
            }, 400