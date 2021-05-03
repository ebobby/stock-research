#!/usr/bin/env python
"""Company summary ORM model."""

from orator import Model, SoftDeletes
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class Summary(SoftDeletes, Model):
    """Company summary ORM model."""

    __dates__ = ["deleted_at"]

    @belongs_to
    def stock(self):
        """The stock ticker for this company."""
        from .stock import Stock

        return Stock
