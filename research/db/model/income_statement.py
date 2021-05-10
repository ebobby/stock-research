#!/usr/bin/env python
"""Income statement ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class IncomeStatement(Model):
    """Income statement ORM model."""

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
