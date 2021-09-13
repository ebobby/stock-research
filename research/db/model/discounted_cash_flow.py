#!/usr/bin/env python
"""Discounted cash flow ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class DiscountedCashFlow(Model):
    """Discounted Cash Flow ORM model."""

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
