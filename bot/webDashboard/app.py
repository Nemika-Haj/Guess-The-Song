from flask import Flask, redirect, url_for, render_template
from core.database import Levels

from core.api import avatar

app = Flask(__name__)

@app.errorhandler(404)
def _404Handler():
    return redirect(url_for('index'))

@app.route("/")
def index(): 
    return render_template("index.html", users=sorted(Levels().get_all(), key=lambda k:k['level'], reverse=True))

def run():
    app.run()