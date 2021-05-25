#!/usr/bin/env python
"""Companies profile ORM model."""

from orator import Model
from orator.orm import belongs_to

__author__ = "Francisco Soto"


class CompanyProfile(Model):
    """Companies profile ORM model."""

    @belongs_to
    def stock(self):
        from . import Stock

        return Stock
