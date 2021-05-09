#!/usr/bin/env python
"""Daily price ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class DailyPrice(Model):
    """Daily price ORM model."""

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
