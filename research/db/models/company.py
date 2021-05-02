#!/usr/bin/env python
"""Companies ORM model."""

from orator import Model, SoftDeletes
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class Company(SoftDeletes, Model):
    """Companies ORM model."""

    __dates__ = ["deleted_at"]

    @belongs_to
    def stock(self):
        """The stock ticker for this company."""
        from .stock import Stock

        return Stock
