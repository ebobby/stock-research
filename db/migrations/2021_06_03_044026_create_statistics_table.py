from orator.migrations import Migration


class CreateStatisticsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("statistics") as table:
            table.big_increments("id")
            table.integer("stock_id").unsigned()

            table.decimal("market_capitalization", 20, 5)
            table.decimal("wallstreet_target_price", 20, 5)
            table.decimal("pe_ratio", 20, 5)
            table.decimal("peg_ratio", 20, 5)
            table.decimal("book_value_per_share", 20, 5)
            table.decimal("earnings_per_share", 20, 5)
            table.decimal("dividend_per_share", 20, 5)
            table.decimal("dividend_yield", 20, 5)
            table.decimal("profit_margin", 20, 5)
            table.decimal("diluted_eps_ttm", 20, 5)
            table.decimal("gross_profit_ttm", 20, 5)
            table.decimal("price_to_sales_ttm", 20, 5)
            table.decimal("operating_margin_ttm", 20, 5)
            table.decimal("return_on_assets_ttm", 20, 5)
            table.decimal("return_on_equity_ttm", 20, 5)
            table.decimal("revenue_per_share_ttm", 20, 5)
            table.decimal("revenue_ttm", 20, 5)
            table.decimal("price_to_book_mrq", 20, 5)
            table.decimal("quarterly_revenue_growth_yoy", 20, 5)
            table.decimal("quarterly_earnings_growth_yoy", 20, 5)

            table.decimal("outstanding_shares", 20, 5)
            table.decimal("floating_shares", 20, 5)
            table.decimal("percent_insiders", 20, 5)
            table.decimal("percent_institutions", 20, 5)
            table.decimal("short_ratio", 20, 5)
            table.decimal("short_percent", 20, 5)

            table.decimal("beta", 20, 5)

            table.decimal("eps_estimate_current_year", 20, 5)
            table.decimal("eps_estimate_next_year", 20, 5)
            table.decimal("eps_estimate_current_quarter", 20, 5)
            table.decimal("eps_estimate_next_quarter", 20, 5)

            table.decimal("growth_estimate_current_quarter", 20, 5)
            table.decimal("growth_estimate_current_year", 20, 5)
            table.decimal("growth_estimate_next_year", 20, 5)

            table.date("most_recent_quarter").nullable()
            table.text("source")

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.unique("stock_id")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("statistics")
