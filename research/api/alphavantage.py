import os

import requests
from requests.exceptions import RequestException


class AlphaVantage:
    """Lightweight wrapper for Alpha Vantage API."""

    API_KEY_ENV = "ALPHAVANTAGE_API_KEY"
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key=None):
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV, "")

    def _call_function(self, function, **kwargs):
        try:
            params = {"apikey": self._api_key, "function": function}
            params = {**kwargs, **params}

            response = requests.get(self.BASE_URL, params)
        except RequestException as e:
            return {"Error Message": str(e)}
        else:
            return response.json()

    def symbol_search(self, keywords):
        """The Search Endpoint returns the best-matching symbols and market information
        based on keywords of your choice."""
        return self._call_function("SYMBOL_SEARCH", keywords=keywords)

    def quote(self, symbol):
        """This service returns the price and volume information for a security of
        your choice."""
        return self._call_function("GLOBAL_QUOTE", symbol=symbol)

    def time_series_daily_adjusted(self, symbol, outputsize="compact"):
        """This API returns raw (as-traded) daily open/high/low/close/volume values,
        daily adjusted close values, and historical split/dividend events of the
        global equity specified, covering 20+ years of historical data."""
        return self._call_function(
            "TIME_SERIES_DAILY_ADJUSTED", symbol=symbol, outputsize=outputsize
        )

    def overview(self, symbol):
        """This API returns the company information, financial ratios, and other key
        metrics for the equity specified."""
        return self._call_function("OVERVIEW", symbol=symbol)

    def earnings(self, symbol):
        """This API returns the annual and quarterly earnings (EPS) for the company
        of interest. Quarterly data also includes analyst estimates and surprise
        metrics."""
        return self._call_function("EARNINGS", symbol=symbol)

    def income_statement(self, symbol):
        """This API returns the annual and quarterly income statements for the company
        of interest."""
        return self._call_function("INCOME_STATEMENT", symbol=symbol)

    def balance_sheet(self, symbol):
        """This API returns the annual and quarterly balance sheets for the company
        of interest."""
        return self._call_function("BALANCE_SHEET", symbol=symbol)

    def cash_flow(self, symbol):
        """This API returns the annual and quarterly cash flows for the company of
        interest."""
        return self._call_function("CASH_FLOW", symbol=symbol)

    def exchange_rate(self, from_currency, to_currency):
        """This API returns the real-time exchange rate for a pair of digital
        currency (e.g., Bitcoin) and physical currency (e.g., USD)."""
        return self._call_function(
            "CURRENCY_EXCHANGE_RATE",
            from_currency=from_currency,
            to_currency=to_currency,
        )
