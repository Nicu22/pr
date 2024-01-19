import pika, sys, os
import threading
from parser import get_product_details
from tinydb import TinyDB
from time import time


db = TinyDB("./db.json")
db.remove(lambda x : True)
lock = threading.Lock()

class Stats:
    def __init__(self):
        self.val = 0
        self.init_time = time()
    def increment(self):
        self.val += 1
    def get(self):
        return f"total parsed: {self.val}, parse per second: {self.val / (time() - self.init_time)}"

stats = Stats()

def client_code(thread_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        product_details = get_product_details(body.decode('UTF-8'))

        try:
            lock.acquire()
            db.insert(product_details)
            stats.increment()
            lock.release()
            print(f"Thread {thread_id}, parsed the link {body}, {stats.get()}")
        except Exception as e:
            print(f"Thread {thread_id}, couldn't parse link {body}")
            print(e)


    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(f"Thread {thread_id} has started")
    channel.start_consuming()


threads = 5
list_threads = []
if threads == 1:
    client_code(0)
for i in range(threads):
    client_thread = threading.Thread(target=client_code, args=(i,))
    client_thread.start()
            