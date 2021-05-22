#!/usr/bin/env python
"""Stock/Shares ORM model."""

from orator import Model
from orator.orm import accessor, has_many

__author__ = "Francisco Soto"


class Stock(Model):
    """Stock/Shares ORM model."""

    @has_many
    def daily_prices(self):
        from .daily_price import DailyPrice

        return DailyPrice

    @has_many
    def income_statements(self):
        from .income_statement import IncomeStatement

        return IncomeStatement

    @has_many
    def balance_sheets(self):
        from .balance_sheet import BalanceSheet

        return BalanceSheet

    @has_many
    def cash_flow_statements(self):
        from .cash_flow_statement import CashFlowStatement

        return CashFlowStatement

    @accessor
    def ticker_for_api(self):
        """Convert ticker to a format that's supported by most API's."""
        ticker = self.ticker

        # Alpha Vantage nor Yahoo Finance like dots.
        ticker = ticker.replace(".", "-")

        # ... nor $, $ becomes -P and every letter after that a -letter.
        if "$" in ticker:
            parts = ticker.split("$")
            ticker = parts[0] + "-P" + "".join([f"-{c}" for c in parts[1]])

        return ticker
