#!/usr/bin/env python
"""Provides syncing facilities to populate and update the database data."""

import logging
from itertools import groupby

from . import nasdaq
from .db.models import Stock
from .logger import getLogger

__author__ = "Francisco Soto"


def nasdaq_stocks():
    """Import symbols from NASDAQ into the database."""
    logger = getLogger("ticker sync")

    def save_list(model, symbols):
        logger.info(f"Syncing {model.__name__.lower()}s into the database.")
        saved = 0
        for symbol in symbols:
            instance = model.where_symbol(symbol[0]).first() or Stock()
            instance.symbol = symbol[0]
            instance.name = symbol[1]

            if instance.save():
                saved += 1
        logger.info(f"{model.__name__} sync finished, saved={saved}.")

    logger.info("Fetching current symbol list from NASDAQ.")

    # Download tickers list from nasdaq and sort them into etfs and stocks.
    stocks, _ = nasdaq.download_traded()

    save_list(Stock, stocks)
