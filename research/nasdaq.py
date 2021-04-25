import logging
import os
import tempfile
from ftplib import FTP

from .logger import getLogger

logger = getLogger("nasdaq")


def download():
    """Download the most recent list of symbols from NASDAQ
    and returns a list of tuples with the data:

    (symbol, name, exchange, etf, status, cqs)"""

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
    symbols = []
    for line in nasdaqtraded:
        parts = line.split("|")
        if parts[7] != "Y":
            symbols.append(
                (
                    parts[1],
                    parts[2],
                    parts[3],
                    parts[5] == "Y",
                    parts[8],
                    parts[9],
                )
            )

    # Remove temporary file.
    os.remove(filename)

    logger.info(f"{len(symbols)} symbols found.")

    # Sort by symbol name.
    return sorted(symbols, key=lambda s: s[0])
