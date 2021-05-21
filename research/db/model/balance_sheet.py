#!/usr/bin/env python
"""Balance sheet ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class BalanceSheet(Model):
    """Balance sheet ORM model."""

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
