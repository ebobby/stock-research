import os

from bottle import TEMPLATE_PATH, Bottle, run, template

from ..db.config import db

dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.append(os.path.join(dir_path, "views"))

app = Bottle()


@app.route("/")
def index():
    rows = (
        db.table("stock_simple_analysis")
        .where("return_on_investment", ">=", 0.15)
        .where("return_on_retained_earnings", ">=", 0.20)
        .order_by("return_on_investment", "DESC")
        .get()
    )
    return template("index", rows=rows)


run(app, host="localhost", port=8080, debug=True)
