from crud_service import Service

service_info = {
    "host" : "127.0.0.1",
    "port" : 8001
}

def main():
    service = Service(service_info, "db1.json")
    print("Service instance created")
    service.init_database()
    print("Database created")
    service.start_http()

main()