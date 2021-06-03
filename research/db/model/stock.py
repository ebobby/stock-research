#!/usr/bin/env python
"""Stock/Shares ORM model."""

from orator import Model
from orator.orm import accessor, has_many, has_one

__author__ = "Francisco Soto"


class Stock(Model):
    """Stock/Shares ORM model."""

    @has_many
    def daily_prices(self):
        from .daily_price import DailyPrice

        return DailyPrice

    @has_many
    def errors(self):
        from .error import Error

        return Error

    @has_one
    def company_profile(self):
        from .company_profile import CompanyProfile

        return CompanyProfile

    @has_one
    def statistics(self):
        from .statistics import Statistics

        return Statistics

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
    def symbol_for_api(self):
        """Convert symbol to a format that's supported by most API's."""
        symbol = self.symbol

        # Alpha Vantage nor Yahoo Finance like dots.
        symbol = symbol.replace(".", "-")

        # ... nor $, $ becomes -P and every letter after that a -letter.
        if "$" in symbol:
            parts = symbol.split("$")
            symbol = parts[0] + "-P" + "".join([f"-{c}" for c in parts[1]])

        return symbol

    def add_error(self, message, source):
        """Add an error to this stock."""
        self.errors().create({"message": message, "source": source})
