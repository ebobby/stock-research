import logging
import os
import sys


def getLogger(name):
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
