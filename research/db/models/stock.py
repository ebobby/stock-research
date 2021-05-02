#!/usr/bin/env python
"""Stock/Shares ORM model."""

from orator import Model, SoftDeletes
from orator.orm import has_one

__author__ = "Francisco Soto"


class Stock(SoftDeletes, Model):
    """Stock/Shares ORM model."""

    __dates__ = ["deleted_at"]

    @has_one
    def company(self):
        """The company represented by this stock."""
        from .company import Company

        return Company
