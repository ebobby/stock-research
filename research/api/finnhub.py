#!/usr/bin/env python
"""Finnhub API wrapper."""

import os
from string import Template

import requests
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException

__author__ = "Francisco Soto"


class Finnhub:
    """Lightweight wrapper for Finnhub API."""

    API_KEY_ENV = "FINNHUB_API_KEY"
    BASE_URL = Template("https://finnhub.io/api/$version/$namespace/$function")

    def __init__(self, api_key=None):
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV, "")

    @sleep_and_retry
    @limits(calls=60, period=60)
    def _call_api(self, version, namespace, function, **kwargs):
        """Make an API call, handles keyword arguments and api keys."""
        url = self.BASE_URL.substitute(
            version=version, namespace=namespace, function=function
        )

        params = {"token": self._api_key}
        params = {**kwargs, **params}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "finnhub/python",
        }

        try:
            response = requests.get(url, params, headers=headers)
        except RequestException as e:
            return {"error": str(e)}
        else:
            if response.status_code != 200:
                return {"error": f"status_code={response.status_code}"}
            return response.json()

    def quote(self, symbol):
        """Get real-time quote data for US stocks."""
        return self._call_api("v1", "quote", "", symbol=symbol.upper())

    def search(self, query):
        """Search for best-matching symbols based on your query. You can input
        anything from symbol, security's name to ISIN and Cusip."""
        return self._call_api("v1", "search", "", q=query)

    def profile(self, symbol="", isin="", cusip=""):
        """Get general information of a company. You can query by symbol, ISIN or
        CUSIP."""
        params = {}
        if cusip:
            params["cusip"] = cusip
        elif isin:
            params["isin"] = isin
        else:
            params["symbol"] = symbol.upper()

        return self._call_api("v1", "stock", "profile", **params)

    def profile2(self, symbol="", isin="", cusip=""):
        """Get general information of a company. You can query by symbol, ISIN or CUSIP.
        This is the free version of Company Profile"""
        params = {}
        if cusip:
            params["cusip"] = cusip
        elif isin:
            params["isin"] = isin
        else:
            params["symbol"] = symbol.upper()

        return self._call_api("v1", "stock", "profile2", **params)

    def executives(self, symbol):
        """Get a list of company's executives and members of the Board."""
        return self._call_api("v1", "stock", "executive", symbol=symbol.upper())

    def market_news(self, category, min_id=0):
        """Get latest market news.

        Arguments:

        `category`  Can be 1 of the following values: general, forex, crypto, merger.
        `min_id`    Use this field to get only news after this ID. Default to 0"""
        return self._call_api("v1", "news", "", category=category, minId=min_id)

    def company_news(self, symbol, fromdate, todate):
        """List latest company news by symbol. This endpoint is only available for
        North American companies.

        Arguments:

        `symbol`        Company symbol.
        `fromdate`      From date YYYY-MM-DD.
        `todate`        To date YYYY-MM-DD."""
        return self._call_api(
            "v1", "company-news", "", symbol=symbol, **{"from": fromdate, "to": todate}
        )

    def press_releases(self, symbol, fromdate, todate):
        """Get latest major press releases of a company. This data can be used to
        highlight the most significant events comprised of mostly press releases
        sourced from the exchanges, BusinessWire, AccessWire, GlobeNewswire, Newsfile,
        and PRNewswire.

        Arguments:

        `symbol`        Company symbol.
        `fromdate`      From date YYYY-MM-DD.
        `todate`        To date YYYY-MM-DD."""
        return self._call_api(
            "v1",
            "press-releases",
            "",
            symbol=symbol,
            **{"from": fromdate, "to": todate},
        )

    def news_sentiment(self, symbol):
        """Get company's news sentiment and statistics. This endpoint is only
        available for US companies."""
        return self._call_api("v1", "news-sentiment", "", symbol=symbol.upper())

    def metrics(self, symbol):
        """Get company basic financials such as margin, P/E ratio, 52-week
        high/low etc."""
        return self._call_api(
            "v1", "stock", "metric", symbol=symbol.upper(), metric="all"
        )

    def ownership(self, symbol, limit=20):
        """Get a full list of shareholders of a company in descending order of the
        number of shares held. Data is sourced from 13F form, Schedule 13D and 13G
        for US market, UK Share Register for UK market, SEDI for Canadian market and
        equivalent filings for other international markets."""
        return self._call_api(
            "v1", "stock", "ownership", symbol=symbol.upper(), limit=20
        )

    def fund_ownership(self, symbol, limit=20):
        """Get a full list fund and institutional investors of a company in
        descending order of the number of shares held. Data is sourced from 13F form,
        Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for
        Canadian market and equivalent filings for other international markets."""
        return self._call_api(
            "v1", "stock", "fund-ownership", symbol=symbol.upper(), limit=20
        )

    def insider_transactions(self, symbol, fromdate, todate):
        """Company insider transactions data sourced from Form 3,4,5. This endpoint
        only covers US companies at the moment. Limit to 100 transactions per API
        call."""
        return self._call_api(
            "v1",
            "stock",
            "insider-transactions",
            symbol=symbol.upper(),
            **{"from": fromdate, "to": todate},
        )

    def financials(self, symbol, statement, freq):
        """Get standardized balance sheet, income statement and cash flow for global
        companies going back 30+ years. Data is sourced from original filings most of
        which made available through SEC Filings and International Filings endpoints.

        Arguments:

        `symbol`    Symbol of the company: AAPL.
        `statement` Statement can take 1 of these values bs, ic, cf for Balance Sheet,
                   Income Statement, Cash Flow respectively.
        `freq`      Frequency can take 1 of these values annual, quarterly, ttm, ytd.
                   TTM (Trailing Twelve Months) option is available for Income Statement
                   and Cash Flow. YTD (Year To Date) option is only available for
                   Cash Flow.
        """
        return self._call_api(
            "v1",
            "stock",
            "financials",
            symbol=symbol.upper(),
            statement=statement,
            freq=freq,
        )
