import logging

from research import nasdaq
from research.db.models import Ticker
from research.logger import getLogger

logger = getLogger("nasdaq")


def symbols():
    """Sync symbols from NASDAQ into the database."""

    logger.info("Fetching current symbol list from NASDAQ.")
    nasdaq_symbols = nasdaq.download()
    logger.info(f"{len(nasdaq_symbols)} fetched.")

    saved = 0
    new = 0
    logger.info("Syncing symbols into the database.")
    for symbol in nasdaq_symbols:
        ticker = Ticker.where("symbol", "=", symbol[0]).first()

        if not ticker:
            ticker = Ticker()
            new += 1

        ticker.symbol = symbol[0]
        ticker.name = symbol[1]
        ticker.exchange = symbol[2]
        ticker.etf = symbol[3]
        ticker.status = symbol[4]
        ticker.cqs = symbol[5]

        if ticker.save():
            saved += 1

    logger.info(f"Tickers sync finished, saved={saved} new={new}.")
