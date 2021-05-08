#!/usr/bin/env python
"""Polygon.io API wrapper."""

import os
from string import Template

import requests
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException

__author__ = "Francisco Soto"


class Polygon:
    """Lightweight wrapper for Polygon.io API."""

    API_KEY_ENV = "POLYGON_API_KEY"
    BASE_URL = Template("https://api.polygon.io/$version/$namespace/$function")

    def __init__(self, api_key=None):
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV, "")

    @sleep_and_retry
    @limits(calls=10, period=60)
    def _call_url(self, url, params={}):
        """Make a GET request to the URL, catches and handles errors."""
        try:
            response = requests.get(url, params)
        except RequestException as e:
            return {"error": str(e)}
        else:
            return response.json()

    def _call_api(self, version, namespace, function, **kwargs):
        """Make an API call, handles keyword arguments and api keys."""
        params = {"apiKey": self._api_key}
        params = {**kwargs, **params}

        url = self.BASE_URL.substitute(
            version=version, namespace=namespace, function=function
        )

        return self._call_url(url, params)

    def _iterate_results(self, response, aggregate=True):
        """Iterate `response` if `aggregate` is `True`. Handles `next_url` responses and
        continues calling the API until it fetches all results."""
        if "error" in response:
            return response

        results = response["results"]

        # Aggregate results.
        while aggregate and "next_url" in response:
            response = self._call_url(response["next_url"], {"apiKey": self._api_key})

            if "error" in response:
                return response

            results.extend(response["results"])

        return results

    def tickers(
        self,
        aggregate=True,
        ticker="",
        ticker_lt="",
        ticker_lte="",
        ticker_gt="",
        ticker_gte="",
        type="",
        market="",
        exchange="",
        cusip="",
        date="",
        active=True,
        sort="ticker",
        order="asc",
        limit=100,
    ):
        """Query all ticker symbols which are supported by Polygon.io. This API
        currently includes Stocks/Equities, Crypto, and Forex.

        If the result returns a `next_url` and `aggregate` is `True` the method will
        aggregate the results till the search is finished."""
        if aggregate:
            limit = 1000

        response = self._call_api(
            "v3",
            "reference",
            "tickers",
            ticker=ticker,
            type=type,
            market=market,
            exchange=exchange,
            cusip=cusip,
            date=date,
            active=active,
            sort=sort,
            order=order,
            limit=limit,
            **{
                "ticker.lt": ticker_lt,
                "ticker.lte": ticker_lte,
                "ticker.gt": ticker_gt,
                "ticker.gte": ticker_gte,
            },
        )

        return self._iterate_results(response, aggregate)

    def ticker_details(self, ticker):
        """Get details for a ticker symbol's company/entity. This provides a general
        overview of the entity with information such as name, sector, exchange, logo
        and similar companies."""
        return self._call_api(
            "v1",
            "meta",
            f"symbols/{ticker}/company",
        )

    def ticker_news(
        self,
        aggregate=True,
        ticker="",
        limit=10,
        order="desc",
        published_utc="",
        sort="published_utc",
        ticker_lt="",
        ticker_lte="",
        ticker_gt="",
        ticker_gte="",
        published_utc_lt="",
        published_utc_lte="",
        published_utc_gt="",
        published_utc_gte="",
    ):
        """Get the most recent news articles relating to a stock ticker symbol,
        including a summary of the article and a link to the original source.

        If the result returns a `next_url` and `aggregate` is `True` the method will
        aggregate the results till the search is finished."""
        if aggregate:
            limit = 1000

        response = self._call_api(
            "v2",
            "reference",
            "news",
            ticker=ticker,
            limit=limit,
            order=order,
            published_utc=published_utc,
            sort=sort,
            **{
                "ticker.lt": ticker_lt,
                "ticker.lte": ticker_lte,
                "ticker.gt": ticker_gt,
                "ticker.gte": ticker_gte,
                "published_utc.lt": published_utc_lt,
                "published_utc.lte": published_utc_lte,
                "published_utc.gt": published_utc_gt,
                "published_utc.gte": published_utc_gte,
            },
        )

        return self._iterate_results(response, aggregate)

    def stock_splits(self, symbol):
        """Get a list of historical stock splits for a ticker symbol, including the
        execution and payment dates of the stock split, and the split ratio."""
        response = self._call_api(
            "v2",
            "reference",
            f"splits/{symbol}",
        )

        return self._iterate_results(response, aggregate=True)

    def stock_dividends(self, symbol):
        """Get a list of historical dividends for a stock, including the relevant
        dates and the amount of the dividend."""
        response = self._call_api(
            "v2",
            "reference",
            f"dividends/{symbol}",
        )

        return self._iterate_results(response, aggregate=True)

    def stock_financials(self, symbol, limit=5, type="Y", sort="-reportPeriod"):
        """Get historical financial data for a stock ticker."""
        response = self._call_api(
            "v2", "reference", f"financials/{symbol}", limit=limit, type=type, sort=sort
        )

        return self._iterate_results(response, aggregate=True)

    def stock_exchanges(self):
        """Get a list of stock exchanges which are supported by Polygon.io."""
        return self._call_api("v1", "meta", "exchanges")
