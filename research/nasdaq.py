#!/usr/bin/env python
"""NASDAQ related utilities."""

import logging
import os
import tempfile
from ftplib import FTP


__author__ = "Francisco Soto"


def download_traded():
    """Download the most recent list of traded tickers from NASDAQ
    and returns a tuple of etfs and stocks with the data: (symbol, name)"""
    logger = logging.getLogger("nasdaq")

    # Nasdaq has a list of all symbols available...
    ftp = FTP("ftp.nasdaqtrader.com")

    # ...login anonymously.
    logger.info("Logging in to ftp.nasdaqtrader.com anonymously...")
    ftp.login()
    ftp.makepasv()

    # Navigate to the symbols directory
    ftp.cwd("Symboldirectory")

    # Create temporary file to hold the data
    handle, filename = tempfile.mkstemp("nasdaqsymbols", text=True)

    # Hold the handle we don't need.
    os.close(handle)

    # Download symbol list
    logger.info("Downloading nasdaqtraded.txt...")
    with open(filename, "wb") as infile:
        ftp.retrbinary("RETR nasdaqtraded.txt", infile.write)

    # Close ftp connection.
    logger.info("Disconecting from ftp.nasdaqtrader.com.")
    ftp.quit()

    # Now let's parse the file.
    logger.info("Parsing downloaded nasdaqtraded.txt...")
    with open(filename, "r") as infile:
        # Skip header and footer.
        nasdaqtraded = infile.readlines()[1:-1]

    # Sample: sample-data/nasdaqtraded.txt
    stocks = []
    etfs = []
    for line in nasdaqtraded:
        parts = line.split("|")

        # If not a test symbol and status is normal then add to list...
        if parts[7] != "Y" and (parts[8] == "" or parts[8] == "N"):
            # etf or stock?
            if parts[5] == "Y":
                etfs.append((parts[1], parts[2]))
            else:
                stocks.append((parts[1], parts[2]))

    # Remove temporary file.
    os.remove(filename)

    logger.info(
        f"{len(etfs) + len(stocks)} symbols found, {len(etfs)} etfs and {len(stocks)} stocks."
    )

    # Sort by symbol name.
    return sorted(stocks), sorted(etfs)
