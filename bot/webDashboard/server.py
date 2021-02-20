from webDashboard import app
from threading import Thread

def start():
    server = Thread(target=app.run)
    server.start()

def debug():
    app.app.run(debug=True)