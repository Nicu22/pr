from flask import Flask, request
app = Flask(__name__)

@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return {
        "Message": "Hello World",
        }
    elif request.method == "POST":
        data = request.json
        print(data)
        return "Confirmation"

app.run()