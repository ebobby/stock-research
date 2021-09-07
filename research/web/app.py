import os

from bottle import TEMPLATE_PATH, Bottle, run, template

from ..db.config import db

dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.append(os.path.join(dir_path, "views"))

ANALYSIS_COLS = [
    "symbol",
    "company_name",
    "url",
    "yahoo_url",
    "market_cap",
    "sector",
    "industry",
    "last_report_date",
    "median_earnings_growth",
    "median_equity_growth",
    "median_return_on_equity",
    "equity_per_share",
    "dividends",
    "eps",
    "eps_5y",
    "eps_10y",
    "earnings",
    "earnings_5y",
    "earnings_10y",
    "eps_cagr_5y",
    "eps_cagr_10y",
    "earnings_cagr_5y",
    "earnings_cagr_10y",
    "accum_dividends",
    "accum_eps",
    "return_on_retained_earnings",
    "last_price",
    "price_date",
    "pe_ratio",
    "avg_pe_ratio",
    "min_pe_ratio",
    "rate_of_return",
    "estimated_eps",
    "estimated_equity_per_share",
    "estimated_rate_of_return",
    "estimated_price_avg_pe",
    "estimated_price_min_pe",
    "roi_avg_pe",
    "roi_min_pe",
]

app = Bottle()


@app.route("/")
def index():
    rows = (
        db.table("stock_buffettology")
        .select(*ANALYSIS_COLS)
        .where("earnings_trend", ">", 0)
        .where("eps_cagr_10y", ">", 0)
        .where("eps_cagr_5y", ">", 0)
        .where_raw("eps_cagr_10y <> 'NAN'::decimal")
        .where_raw("eps_cagr_5y <> 'NAN'::decimal")
        .where("has_errors", "=", "f")
        .where("currency", "=", "USD")
        .where("category", "ilike", "%domestic%")
        .where("median_return_on_equity", ">", 0)
        .where("median_equity_growth", ">", 0)
        .where("median_earnings_growth", ">", 0)
        .where("roi_min_pe", ">=", 0.15)
        .where("return_on_retained_earnings", ">=", 0.20)
        .order_by("roi_min_pe", "DESC")
        .get()
    )
    return template("index", rows=rows)


run(app, host="localhost", port=8080)
