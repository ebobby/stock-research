#!/usr/bin/env python
"""Stock/Shares ORM model."""

from orator import Model, SoftDeletes
from orator.orm import accessor

__author__ = "Francisco Soto"


class Stock(SoftDeletes, Model):
    """Stock/Shares ORM model."""

    __dates__ = ["deleted_at"]

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
