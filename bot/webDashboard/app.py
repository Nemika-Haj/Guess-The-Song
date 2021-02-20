from flask import Flask, redirect, url_for
from ..core.database import Levels

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view/", defaults={"userID":None})
@app.route("/view/<userID>")
def viewProfile(userID):
    if not userID:
        return redirect(url_for('index'))
    else:
        return render_template('view.html', Levels(int(userID)).get())

def run():
    app.run(debug=True)