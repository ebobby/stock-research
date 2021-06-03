#!/usr/bin/env python
"""Stock statistics and analysis ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class Statistics(Model):
    """Stock statistics and analysis ORM model."""

    __table__ = "statistics"

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
