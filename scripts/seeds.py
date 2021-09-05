#!/usr/bin/env python
"""Functions to populate the database for the first time."""

from datetime import date, timedelta

from research import importer
from research.db.config import db

__author__ = "Francisco Soto"


def init():
    # Import all available stocks.
    importer.stocks()
    # Get all fundamental data for these stocks.
    importer.fundamentals()

    # Import latest stock prices.
    delta = 0
    while not importer.prices(date.today() - timedelta(days=delta)):
        delta += 1

    # Import stock prices for PE calculations
    dates = list(
        db.table("income_statements")
        .select_raw("distinct report_date")
        .where_raw("report_date < NOW() and report_type = 'Y'")
        .get()
    )

    # Import closest price after each yearly report so we can have a price to
    # calculate PE ratio
    for day in sorted(dates):
        delta = 0
        while not importer.prices(day[0] + timedelta(days=delta)):
            delta += 1
