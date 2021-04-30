#!/usr/bin/env python
"""Etf database ORM model."""

from orator import Model, SoftDeletes

__author__ = "Francisco Soto"


class Etf(SoftDeletes, Model):
    """Exchange traded fund ORM model."""

    __dates__ = ["deleted_at"]

    @staticmethod
    def by_symbol_or_new(symbol):
        """Find ETF by symbol or return a new object."""
        return Etf.where("symbol", "=", symbol).first() or Etf()
