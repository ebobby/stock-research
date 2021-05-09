#!/usr/bin/env python
"""Stock/Shares ORM model."""

from orator import Model
from orator.orm import accessor, has_many

__author__ = "Francisco Soto"


class Stock(Model):
    """Stock/Shares ORM model."""

    @has_many
    def daily_prices(self):
        from .daily_price import DailyPrice

        return DailyPrice

    @accessor
    def ticker_for_alpha_vantage(self):
        """Convert ticker to a format that's supported by Alpha Vantage."""
        ticker = self.ticker

        # Alpha Vantage nor Yahoo Finance like dots.
        ticker = ticker.replace(".", "-")

        # ... nor $, $ becomes -P and every letter after that a -letter.
        if "$" in ticker:
            parts = ticker.split("$")
            ticker = parts[0] + "-P" + "".join([f"-{c}" for c in parts[1]])

        return ticker
