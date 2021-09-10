import os

from bottle import TEMPLATE_PATH, Bottle, run, template

from ..db.config import db
from ..db.model import Stock

dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.append(os.path.join(dir_path, "views"))

app = Bottle()


@app.route("/")
def index():
    rows = (
        db.table("stock_simple_analysis")
        .where("annual_return", ">=", 0.15)
        .where("validation", "<", 1.50)
        .where("validation", ">", 0.0)
        .order_by("annual_return", "DESC")
        .get()
    )
    return template("index", rows=rows)


@app.route("/stock/<symbol>")
def stock(symbol):
    averages = db.table("stock_annual_averages").where("symbol", "=", symbol).first()

    buffettology = db.table("stock_buffettology").where("symbol", "=", symbol).first()

    annual = (
        db.table("stock_annual_report")
        .where("symbol", "=", symbol)
        .order_by("date", "desc")
        .get()
    )

    stats = (
        db.table("statistics")
        .select("statistics.*")
        .join("stocks", "stocks.id", "=", "statistics.stock_id")
        .where("stocks.symbol", "=", symbol)
        .first()
    )

    prices = (
        db.table("daily_prices")
        .select("date", "open", "high", "low", "close", "volume")
        .join("stocks", "stocks.id", "=", "daily_prices.stock_id")
        .where("stocks.symbol", "=", symbol)
        .limit(5)
        .order_by("date", "desc")
        .get()
    )

    return template(
        "stock",
        symbol=symbol,
        averages=averages,
        buffettology=buffettology,
        stats=stats,
        annual=annual,
        prices=prices,
    )


run(app, host="localhost", port=8080, debug=True)
