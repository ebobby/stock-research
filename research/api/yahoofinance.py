#!/usr/bin/env python
"""Yahoo Finance Scrapper."""
from string import Template

import requests
from parsel import Selector
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException

__author__ = "Francisco Soto"


class YahooFinance:
    """Yahoo Finance Scrapper."""

    BASE_URL = Template("https://finance.yahoo.com/$namespace/$function")

    @sleep_and_retry
    @limits(calls=60, period=60)
    def _call_page(self, namespace, function, **kwargs):
        """Make an API call, handles keyword arguments and api keys."""
        url = self.BASE_URL.substitute(namespace=namespace, function=function)

        try:
            response = requests.get(url, kwargs)
        except RequestException:
            return ""
        else:
            if response.status_code != 200:
                return ""
            return response.content.decode("utf-8")

    def estimated_growth(self, symbol=None):
        """Estimated yearly growth for the given symbol."""

        def parse_value(value):
            if value and value != "N/A":
                try:
                    return round(float(value[0:-1]) / 100.0, 5)
                except ValueError:
                    return None
            return None

        page = Selector(
            text=self._call_page(
                f"quote/{symbol.upper()}", "analysis", p=symbol.upper()
            )
        )

        return {
            "current_quarter": parse_value(
                page.css('td[data-reactid="399"]::text').get()
            ),
            "next_quarter": parse_value(page.css('td[data-reactid="406"]::text').get()),
            "current_year": parse_value(page.css('td[data-reactid="413"]::text').get()),
            "next_year": parse_value(page.css('td[data-reactid="420"]::text').get()),
            "next_five_years": parse_value(
                page.css('td[data-reactid="427"]::text').get()
            ),
            "past_five_years": parse_value(
                page.css('td[data-reactid="434"]::text').get()
            ),
        }
