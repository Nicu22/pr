from requests_html import HTMLSession
import requests

session = HTMLSession()

URL = "http://127.0.0.1:5000/hello"
data = session.get(URL)
print(data)

data = requests.post(URL, json = {"message" : "Hello back"})
print(data.text)