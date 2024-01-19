import pika
import requests
from bs4 import BeautifulSoup

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='hello')

class Integer:
    def __init__(self):
        self.val = 0
    def increment(self):
        self.val += 1
    def get_value(self):
        return self.val

total_links = Integer()
_links = []

def recursion(_URL, max_pages=100, current_page=1):

    #max page handling
    if(max_pages == current_page - 1):
        return
    
    #html handling
    r = requests.get(_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.find_all("a", href=True, class_="js-item-ad")
    for link in a:
        if('/ro/' in link["href"]):
            full_link = "https://999.md" + link["href"]
            if(full_link not in _links):
                try:
                    channel.basic_publish(exchange='', routing_key='hello', body=full_link)
                    total_links.increment()
                    print(f"{total_links.get_value()} links published")
                    _links.append(full_link)
                except:
                    print(f"Something happened to {full_link}")
                    pass

    #next page handling
    nav = soup.find("nav", class_="paginator cf")
    li = nav.ul.find_all("li")
    page_URL = None
    for i in li:
        if(str(current_page) in i.text):
            page_URL = "https://999.md" + i.find("a")["href"]
            break
    
    #if no next page, finish recursion
    if page_URL == None:
        return
    
    return recursion(page_URL, max_pages, current_page=current_page+1)

recursion("https://999.md/ro/list/computers-and-office-equipment/video")

connection.close()