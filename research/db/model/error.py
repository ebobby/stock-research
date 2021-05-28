#!/usr/bin/env python
"""Error (in data) ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class Error(Model):
    """Error (in data) ORM model."""

    __fillable__ = ["message", "source"]

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
