from flask import Flask, redirect, url_for, render_template
from core.database import Levels

from core.api import avatar

app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html", users=sorted(Levels(1).get_all()[1:], key=lambda k:k['level'], reverse=True))

@app.route("/view/", defaults={"userID":None})
@app.route("/view/<userID>")
def viewProfile(userID):
    if not userID:
        return redirect(url_for('index'))
    else:
        return render_template('view.html', Levels(int(userID)).get())

def run():
    app.run()