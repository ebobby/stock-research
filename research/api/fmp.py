#!/usr/bin/env python
"""Financial Modeling Prep API wrapper."""

import os
from string import Template

import requests
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException

__author__ = "Francisco Soto"


class FMP:
    """Lightweight wrapper for Financial Modeling Prep API."""

    API_KEY_ENV = "FMP_API_KEY"
    BASE_URL = Template("https://financialmodelingprep.com/api/$version/$function")

    def __init__(self, api_key=None):
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV, "")

    @sleep_and_retry
    @limits(calls=300, period=60)
    def _call_api(self, version, function, **kwargs):
        """Make an API call, handles keyword arguments and api keys."""
        params = {"apikey": self._api_key}
        params = {**kwargs, **params}

        url = self.BASE_URL.substitute(version=version, function=function)

        try:
            response = requests.get(url, params)
        except RequestException as e:
            return {"error": str(e)}
        else:
            return response.json()

    def quote(self, ticker):
        """Company quote."""
        return self._call_api("v3", f"quote/{ticker.upper()}")

    def company_profile(self, ticker):
        """Companies profile."""
        return self._call_api("v3", f"profile/{ticker.upper()}")

    def company_executives(self, ticker):
        """Company key executives."""
        return self._call_api("v3", f"key-executives/{ticker.upper()}")

    def ticker_search(self, query, exchange, limit=100):
        """Search via ticker and company name.

        Values for exchange parameter are: ETF | MUTUAL_FUND | COMMODITY | INDEX |
        CRYPTO | FOREX | TSX | AMEX | NASDAQ | NYSE | EURONEXT | XETRA | NSE | LSE"""
        return self._call_api(
            "v3", "search", query=query, exchange=exchange, limit=limit
        )

    def income_statement(self, ticker, period="year", limit=10):
        """This API returns the annual and quarterly income statements for the company."""
        return self._call_api(
            "v3",
            f"income-statement/{ticker.upper()}",
            period=period,
            limit=limit,
        )

    def balance_sheet(self, ticker, period="year", limit=10):
        """This API returns the annual and quarterly balance sheets for the company."""
        return self._call_api(
            "v3",
            f"balance-sheet-statement/{ticker.upper()}",
            period=period,
            limit=limit,
        )

    def cash_flow(self, ticker, period="year", limit=10):
        """This API returns the annual and quarterly cash flows for the company."""
        return self._call_api(
            "v3",
            f"cash-flow-statement/{ticker.upper()}",
            period=period,
            limit=limit,
        )
