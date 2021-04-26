import logging

from . import nasdaq
from .db.models import Ticker
from .logger import getLogger

logger = getLogger("sync")


def symbols():
    """Sync symbols from NASDAQ into the database."""

    logger.info("Fetching current symbol list from NASDAQ.")
    nasdaq_symbols = nasdaq.download()
    logger.info(f"{len(nasdaq_symbols)} fetched.")

    logger.info("Syncing symbols into the database.")
    saved = 0
    for symbol in nasdaq_symbols:
        ticker = Ticker.by_symbol_or_new(symbol[0])

        ticker.symbol = symbol[0]
        ticker.name = symbol[1]
        ticker.exchange = symbol[2]
        ticker.etf = symbol[3]
        ticker.status = symbol[4]
        ticker.cqs = symbol[5]

        if ticker.save():
            saved += 1

    logger.info(f"Tickers sync finished, saved={saved}.")
