#!/usr/bin/env python
"""Companies ORM model."""

from orator import Model, SoftDeletes

__author__ = "Francisco Soto"


class Company(SoftDeletes, Model):
    """Companies ORM model."""

    __dates__ = ["deleted_at"]
