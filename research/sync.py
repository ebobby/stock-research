import logging
from itertools import groupby

from . import nasdaq
from .db.models import Etf, Stock
from .logger import getLogger

logger = getLogger("sync")


def symbols():
    """Sync symbols from NASDAQ into the database."""

    def save_list(model, symbols):
        logger.info(f"Syncing {model.__name__.lower()}s into the database.")
        saved = 0
        for symbol in symbols:
            instance = model.by_symbol_or_new(symbol[0])
            instance.symbol = symbol[0]
            instance.name = symbol[1]

            if instance.save():
                saved += 1
        logger.info(f"{model.__name__} sync finished, saved={saved}.")

    logger.info("Fetching current symbol list from NASDAQ.")

    # Download tickers list from nasdaq and sort them into etfs and stocks.
    stocks, etfs = nasdaq.download()

    save_list(Stock, stocks)
    save_list(Etf, etfs)
