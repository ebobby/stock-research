#!/usr/bin/env python
"""EOD Historical Data API wrapper."""

import os
from string import Template

import requests
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException

__author__ = "Francisco Soto"


class EOD:
    """Lightweight wrapper for EOD Historical Data API."""

    API_KEY_ENV = "EOD_API_KEY"
    BASE_URL = Template("https://eodhistoricaldata.com/api/$namespace/$function")

    def __init__(self, api_key=None):
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV, "")

    @sleep_and_retry
    @limits(calls=2000, period=60)
    def _call_api(self, namespace, function, **kwargs):
        """Make an API call, handles keyword arguments and api keys."""
        url = self.BASE_URL.substitute(namespace=namespace, function=function)

        params = {"api_token": self._api_key}
        params = {**kwargs, **params}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, params, headers=headers)
        except RequestException as e:
            return {"error": str(e)}
        else:
            if response.status_code != 200:
                return {"error": f"status_code={response.status_code}"}
            return response.json()

    def exchanges_list(self):
        """Get the full list of supported exchanges with names, codes, operating MICs,
        country, and currency."""
        return self._call_api("exchanges-list", "", fmt="json")

    def exchange_symbol_list(self, exchange="US"):
        """Get a list of symbols for the given exchange."""
        return self._call_api("exchange-symbol-list", exchange.upper(), fmt="json")

    def eod(
        self,
        symbol,
        exchange="US",
        period="d",
        order="a",
        fromdate="",
        todate="",
    ):
        """End-of-day data feed."""
        return self._call_api(
            "eod",
            f"{symbol.upper()}.{exchange.upper()}",
            period=period,
            order=order,
            **{"from": fromdate, "to": todate},
            fmt="json",
        )

    def fundamentals(self, symbol, exchange="US"):
        """Fundamentals data feed."""
        return self._call_api("fundamentals", f"{symbol.upper()}.{exchange.upper()}")

    def bulk_fundamentals(self, exchange, symbols=None):
        """Bulk fundamentals data feed."""
        return self._call_api(
            "bulk-fundamentals", exchange.upper(), symbols=symbols, fmt="json"
        )

    def bulk_eod(self, exchange, date=None, symbols=None, filter=None):
        """Bulk end-of-day prices data feed."""
        return self._call_api(
            "eod-bulk-last-day",
            exchange.upper(),
            date=date,
            symbols=symbols,
            filter=filter,
            fmt="json",
        )
