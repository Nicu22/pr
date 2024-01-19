from flask import Flask, request

def do_routing(service):
    service.app = Flask(__name__)

    @service.app.route("/product", methods=["GET"])
    def get():
        return service.read_product(request)

    @service.app.route("/product", methods=["PUT"])
    def put():
        return service.update_product(request)

    @service.app.route("/product", methods=["DELETE"])
    def delete():
        return service.delete_product(request)

    @service.app.route("/product", methods=["POST"])
    def post():
        return service.create_product(request)