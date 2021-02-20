from app import 
from threading import Thread

def start():
    server = Thread(target=app.run())
    server.start()