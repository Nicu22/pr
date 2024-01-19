from crud_service import Service

service_info = {
    "host" : "127.0.0.1",
    "port" : 8000
}

def main():
    service = Service(service_info, "db0.json")
    print("Service instance created")
    service.init_database()
    service.start_http()

main()