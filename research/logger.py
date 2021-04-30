#!/usr/bin/env python
"""Logging facilities."""

import logging
import os
import sys

__author__ = "Francisco Soto"


def getLogger(name):
    """Returns a tagged logger object that outputs to STDOUT."""
    logger = logging.getLogger(name)

    logger.setLevel(
        logging.INFO if os.environ.get("stage") == "production" else logging.DEBUG
    )

    handler = None
    formatter = logging.Formatter(
        f"%(asctime)s [%(name)s] [%(levelname)s] --: %(message)s"
    )

    if not handler:
        if logger.hasHandlers():
            handler = logger.handlers[0]
        else:
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)

    handler.setFormatter(formatter)

    return logger
