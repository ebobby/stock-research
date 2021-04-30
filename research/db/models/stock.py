#!/usr/bin/env python
"""Stock/Shares ORM model."""

from orator import Model, SoftDeletes

__author__ = "Francisco Soto"


class Stock(SoftDeletes, Model):
    """Stock/Shares ORM model."""

    __dates__ = ["deleted_at"]

    @staticmethod
    def by_symbol_or_new(symbol):
        """Find stock by symbol or return a new object."""
        return Stock.where("symbol", "=", symbol).first() or Stock()
