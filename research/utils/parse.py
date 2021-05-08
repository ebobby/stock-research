#!/usr/bin/env python
"""Parsing facilities."""

from datetime import datetime

__author__ = "Francisco Soto"


def str_or(value, default=None):
    """Tries to parse `value` to string, returns `default` if failure."""
    try:
        return str(value)
    except:
        return default


def int_or(value, default=None):
    """Tries to parse `value` to integer, returns `default` if failure."""
    try:
        return int(value)
    except:
        return default


def float_or(value, default=None):
    """Tries to parse `value` to float, returns `default` if failure."""
    try:
        return float(value)
    except:
        return default


def date_or(value, fmt, default=None):
    """Tries to parse `value` to date in `format`, returns `default` if failure."""
    try:
        return datetime.strptime(value, fmt).date()
    except:
        return default
