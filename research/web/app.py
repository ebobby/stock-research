import os

from bottle import TEMPLATE_PATH, Bottle, request, run, template

from ..db.config import db

dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.append(os.path.join(dir_path, "views"))

app = Bottle()


@app.route("/")
def index():
    annual_return = (
        request.query["annual_return"] if "annual_return" in request.query else 0.15
    )

    rows = (
        db.table("stock_simple_analysis")
        .where("annual_return", ">=", float(annual_return))
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

    quarters = (
        db.table("stock_quarterly_report")
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

    profile = (
        db.table("company_profiles")
        .select("company_profiles.*")
        .join("stocks", "stocks.id", "=", "company_profiles.stock_id")
        .where("stocks.symbol", "=", symbol)
        .first()
    )

    prices = (
        db.table("daily_prices")
        .select("date", "open", "high", "low", "close", "volume")
        .join("stocks", "stocks.id", "=", "daily_prices.stock_id")
        .where("stocks.symbol", "=", symbol)
        .limit(10)
        .order_by("date", "desc")
        .get()
    )

    dcfs = (
        db.table("discounted_cash_flows")
        .select(
            "last_date",
            "discount_rate",
            "discounted_cash_flows",
            "discounted_share_price",
        )
        .join("stocks", "stocks.id", "=", "discounted_cash_flows.stock_id")
        .where("stocks.symbol", "=", symbol)
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
        dcfs=dcfs,
        profile=profile,
        quarters=quarters,
    )


run(app, host="localhost", port=8080, debug=True)
