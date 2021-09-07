from bottle import Bottle, run

from ..db.config import db

app = Bottle()


@app.route("/")
def index():
    return "Hello World!"


run(app, host="localhost", port=8080)
