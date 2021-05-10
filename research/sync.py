#!/usr/bin/env python
"""Provides syncing facilities to populate and update the database data."""

import logging
from datetime import date, datetime, timedelta
from itertools import groupby

from orator.exceptions.query import QueryException

from . import nasdaq
from .api import AlphaVantage, Polygon
from .db import db
from .db.model import DailyPrice, IncomeStatement, Stock
from .logger import getLogger
from .utils import parse

__author__ = "Francisco Soto"


def stocks():
    """Import stocks from Polygon.io into the database."""
    logger = getLogger("stock sync")

    # Polygon.io API
    api = Polygon()

    logger.info("Stock sync started")

    # Fetch all available stocks
    logger.info("Fetching current stock list from Polygon.io")
    tickers = api.tickers(aggregate=True, type="CS", limit=1000)
    logger.info(f"{len(tickers)} active stocks found")

    # Fetching exchanges
    logger.info("Fetching supported exchnages list from Polygon.io")
    exchanges = api.stock_exchanges()
    logger.info(f"{len(exchanges)} exchanges found")

    exchange_map = {e["mic"]: e["name"] for e in exchanges if "mic" in e}

    # First set all stocks to inactive.
    db.table("stocks").update(active=False)

    # Update all tickers
    for ticker in tickers:
        stock = Stock.where_ticker(ticker["ticker"]).first() or Stock()

        stock.ticker = ticker["ticker"]
        stock.name = ticker["name"]
        stock.locale = ticker["locale"]
        stock.currency = ticker["currency_name"]
        stock.exchange = exchange_map.get(
            ticker["primary_exchange"], ticker["primary_exchange"]
        )
        stock.cik = ticker.get("cik", "")
        stock.active = ticker["active"]

        stock.save()

    active = Stock.where_active(True).count()
    inactive = Stock.where_active(False).count()

    logger.info(
        f"Stock sync finished, {active} active stocks, {inactive} inactive stocks"
    )


def prices():
    """Import historical stock prices from AlphaVantage into the database."""

    logger = getLogger("price sync")

    logger.info("Price sync starting")

    # AlphaVantage.co API
    api = AlphaVantage()

    stocks = list(Stock.where_active(True).get())
    logger.info(f"{len(stocks)} active stocks found")

    report_time = datetime.timestamp(datetime.now())
    processed = 0
    saved = 0
    skipped = 0

    # Figure out the last week day (can be today).
    prev_weekday = date.today()
    if prev_weekday.weekday() > 4:
        prev_weekday -= timedelta(prev_weekday.weekday() - 4)

    for stock in stocks:
        last_saved = stock.daily_prices().order_by("date", "desc").first()

        if last_saved and last_saved.date == prev_weekday:
            skipped += 1
            continue

        # Fetch time series
        timeseries = api.time_series_daily_adjusted(
            stock.ticker_for_alpha_vantage, outputsize="full"
        )

        if not timeseries or "Error Message" in timeseries:
            logger.warning(f"Failed to find daily prices for {stock.ticker}")
            continue

        # Convert time series into a more manageable format.
        timeseries = sorted(
            [
                {"date": day, **timeseries["Time Series (Daily)"][day]}
                for day in timeseries["Time Series (Daily)"].keys()
            ],
            key=lambda ts: ts["date"],
        )

        # Build a set with ticker prices we already have.
        current_prices = {
            dp.strftime(AlphaVantage.DATE_FORMAT)
            for dp in stock.daily_prices().get().pluck("date")
        }

        for datapoint in timeseries:
            if datapoint["date"] not in current_prices:
                dp = DailyPrice()
                dp.date = parse.date_or(datapoint["date"], AlphaVantage.DATE_FORMAT)
                dp.open = parse.float_or(datapoint["1. open"], 0.0)
                dp.high = parse.float_or(datapoint["2. high"], 0.0)
                dp.low = parse.float_or(datapoint["3. low"], 0.0)
                dp.close = parse.float_or(datapoint["4. close"], 0.0)
                dp.adjusted_close = parse.float_or(datapoint["5. adjusted close"], 0.0)
                dp.volume = parse.int_or(datapoint["6. volume"], 0)
                dp.dividends = parse.float_or(datapoint["7. dividend amount"], 0.0)
                dp.split_coefficient = parse.float_or(
                    datapoint["8. split coefficient"], 0.0
                )

                stock.daily_prices().save(dp)
                saved += 1

        processed += 1

        # Report current progress
        if datetime.timestamp(datetime.now()) - report_time >= 60:
            logger.info(
                f"{processed} stocks processed, {skipped} skipped and {saved} daily prices saved"
            )
            report_time = datetime.timestamp(datetime.now())

    logger.info(
        f"Price sync finished, {processed} stocks processed, {skipped} skipped and {saved} daily prices saved"
    )


def income_statements():
    """Import historical income statements from AlphaVantage into the database."""
    logger = getLogger("income statement sync")

    def process_reports(stock, report_type, reports, current):
        saved = 0

        for report in reports:
            if report["fiscalDateEnding"] in current:
                continue

            # These two seem to be mixed up sometimes, pick the largest one.
            cost_of_revenue = parse.int_or(report["costOfRevenue"], 0)
            cost_of_goods = parse.int_or(report["costofGoodsAndServicesSold"], 0)
            cost_of_revenue = max([cost_of_goods, cost_of_revenue])

            gross_profit = parse.int_or(report["grossProfit"], 0)
            total_revenue = parse.int_or(report["totalRevenue"], 0)

            ins = IncomeStatement()
            ins.report_type = report_type
            ins.fiscal_date = parse.date_or(
                report["fiscalDateEnding"], AlphaVantage.DATE_FORMAT
            )
            ins.currency = parse.str_or(report["reportedCurrency"], "")
            ins.total_revenue = total_revenue
            ins.cost_of_revenue = cost_of_revenue
            ins.gross_profit = gross_profit
            ins.operating_income = parse.int_or(report["operatingIncome"], 0)
            ins.income_before_tax = parse.int_or(report["incomeBeforeTax"], 0)
            ins.income_tax = parse.int_or(report["incomeTaxExpense"], 0)
            ins.net_income_from_operations = parse.int_or(
                report["netIncomeFromContinuingOperations"], 0
            )
            ins.net_income = parse.int_or(report["netIncome"], 0)

            try:
                stock.income_statements().save(ins)
                saved += 1
            except QueryException:
                logger.error(
                    f"Duplicate report {(report['fiscalDateEnding'], report_type)} found for {stock.ticker}"
                )

        return saved

    logger.info("Income statement sync starting")

    # AlphaVantage.co API
    api = AlphaVantage()

    stocks = list(Stock.where_active(True).order_by("ticker").get())
    logger.info(f"{len(stocks)} active stocks found")

    report_time = datetime.timestamp(datetime.now())
    processed = 0
    saved = 0
    skipped = 0

    today = date.today()

    for stock in stocks:
        skip_yearly = False
        skip_quarterly = False

        last_yearly = (
            stock.income_statements()
            .where_report_type("Y")
            .order_by("fiscal_date", "desc")
            .first()
        )
        last_quarterly = (
            stock.income_statements()
            .where_report_type("Y")
            .order_by("fiscal_date", "desc")
            .first()
        )

        skip_yearly = last_yearly and (today - last_yearly.fiscal_date).days < 365
        skip_quarterly = (
            last_quarterly and (today - last_quarterly.fiscal_date).days < 91
        )

        if skip_quarterly and skip_yearly:
            skipped += 1
            continue

        # Fetch income statements
        statements = api.income_statement(stock.ticker_for_alpha_vantage)

        if not statements or "Error Message" in statements:
            logger.warning(f"Failed to find income statements for {stock.ticker}")
            continue

        annual = statements["annualReports"]
        quarterly = statements["quarterlyReports"]

        if not skip_yearly:
            # Build a set with statements we already have.
            current_annual = {
                fd.strftime(AlphaVantage.DATE_FORMAT)
                for fd in stock.income_statements()
                .where_report_type("Y")
                .get()
                .pluck("fiscal_date")
            }
            saved += process_reports(stock, "Y", annual, current_annual)

        if not skip_quarterly:
            # Build a set with statements we already have.
            current_quarterly = {
                fd.strftime(AlphaVantage.DATE_FORMAT)
                for fd in stock.income_statements()
                .where_report_type("Q")
                .get()
                .pluck("fiscal_date")
            }
            saved += process_reports(stock, "Q", quarterly, current_quarterly)

        processed += 1

        # Report current progress
        if datetime.timestamp(datetime.now()) - report_time >= 60:
            logger.info(
                f"{processed} stocks processed, {skipped} skipped. {saved} income statements saved"
            )
            report_time = datetime.timestamp(datetime.now())

    logger.info(
        f"Income statement sync finished, {processed} stocks processed, {skipped} skipped. {saved} income statements saved"
    )
