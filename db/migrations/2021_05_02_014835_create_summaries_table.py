from orator.migrations import Migration


class CreateSummariesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("summaries") as table:
            table.increments("id")

            table.integer("stock_id").unsigned()
            table.foreign("stock_id").references("id").on("stocks")

            table.date("latest_quarter")
            table.unique(["stock_id", "latest_quarter"])

            table.big_integer("market_capitalization").nullable()

            table.decimal("beta", 16, 4).nullable()
            table.decimal("book_value", 16, 4).nullable()
            table.big_integer("ebitda").nullable()
            table.decimal("eps", 16, 4).nullable()
            table.decimal("ev_to_ebitda", 16, 4).nullable()
            table.decimal("ev_to_revenue", 16, 4).nullable()
            table.decimal("forward_pe", 16, 4).nullable()
            table.decimal("pe_ratio", 16, 4).nullable()
            table.decimal("peg_ratio", 16, 4).nullable()
            table.decimal("price_to_book_ratio", 16, 4).nullable()
            table.decimal("profit_margin", 16, 4).nullable()
            table.decimal("trailing_pe", 16, 4).nullable()

            table.decimal("diluted_eps_ttm", 16, 4).nullable()
            table.big_integer("gross_profit_ttm").nullable()
            table.decimal("operating_margin_ttm", 16, 4).nullable()
            table.decimal("price_to_sales_ratio_ttm", 16, 4).nullable()
            table.decimal("quaterly_earnings_growth_yoy", 16, 4).nullable()
            table.decimal("quaterly_revenue_growth_yoy", 16, 4).nullable()
            table.decimal("return_on_assets_ttm", 16, 4).nullable()
            table.decimal("return_on_equity_ttm", 16, 4).nullable()
            table.decimal("revenue_per_share_ttm", 16, 4).nullable()
            table.big_integer("revenue_ttm").nullable()

            table.decimal("200_day_moving_average", 16, 4).nullable()
            table.decimal("50_day_moving_average", 16, 4).nullable()
            table.decimal("52_week_high", 16, 4).nullable()
            table.decimal("52_week_low", 16, 4).nullable()

            table.big_integer("shares_float").nullable()
            table.big_integer("shares_outstanding").nullable()
            table.big_integer("shares_short").nullable()
            table.big_integer("shares_short_prior_month").nullable()

            table.decimal("short_ratio", 16, 4).nullable()
            table.decimal("short_percent_outstanding", 16, 4).nullable()
            table.decimal("short_percent_float", 16, 4).nullable()

            table.decimal("dividend_per_share", 16, 4).nullable()
            table.decimal("dividend_yield", 16, 4).nullable()
            table.decimal("payout_ratio", 16, 4).nullable()
            table.decimal("forward_annual_dividend_rate", 16, 4).nullable()
            table.decimal("forward_annual_dividend_yield", 16, 4).nullable()
            table.date("dividend_date").nullable()
            table.date("ex_dividend_date").nullable()

            table.text("last_split_factor").nullable()
            table.date("last_split_date").nullable()

            table.decimal("analyst_target_price", 16, 4).nullable()
            table.decimal("percent_insiders", 16, 4).nullable()
            table.decimal("percent_institutions", 16, 4).nullable()

            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("summaries")
