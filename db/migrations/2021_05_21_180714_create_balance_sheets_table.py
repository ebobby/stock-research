from orator.migrations import Migration


class CreateBalanceSheetsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("balance_sheets") as table:
            table.big_increments("id")

            table.integer("stock_id").unsigned()
            table.date("report_date")
            table.char("report_type", 2)
            table.text("currency").nullable()

            table.date("filing_date")

            table.decimal("total_assets", 20, 5)
            table.decimal("total_current_assets", 20, 5)
            table.decimal("cash_and_short_term", 20, 5)
            table.decimal("inventory", 20, 5)
            table.decimal("receivables", 20, 5)
            table.decimal("other_current_assets", 20, 5)

            table.decimal("total_non_current_assets", 20, 5)
            table.decimal("property_plant_equipment", 20, 5)
            table.decimal("good_will", 20, 5)
            table.decimal("intangible_assets", 20, 5)
            table.decimal("long_term_investments", 20, 5)
            table.decimal("other_non_current_assets", 20, 5)

            table.decimal("total_liabilities", 20, 5)

            table.decimal("total_current_liabilities", 20, 5)
            table.decimal("accounts_payable", 20, 5)
            table.decimal("short_term_debt", 20, 5)
            table.decimal("other_current_liabilities", 20, 5)

            table.decimal("total_non_current_liabilities", 20, 5)
            table.decimal("long_term_debt", 20, 5)
            table.decimal("deferred_long_term_liabilities", 20, 5)
            table.decimal("other_non_current_liabilities", 20, 5)

            table.decimal("total_stockholder_equity", 20, 5)
            table.decimal("preferred_stock_equity", 20, 5)
            table.decimal("common_stock_equity", 20, 5)
            table.decimal("paid_in_capital", 20, 5)
            table.decimal("retained_earnings", 20, 5)
            table.decimal("treasury_stock", 20, 5)
            table.decimal("gain_losses", 20, 5)
            table.decimal("non_controlling_interest", 20, 5)

            table.decimal("total_capitalization", 20, 5)

            table.decimal("capital_lease_obligations", 20, 5)
            table.decimal("net_tangible_assets", 20, 5)
            table.decimal("net_working_capital", 20, 5)
            table.decimal("net_invested_capital", 20, 5)
            table.decimal("short_long_term_debt_total", 20, 5)
            table.decimal("net_debt", 20, 5)

            table.decimal("common_stock_shares_outstanding", 20, 5)

            table.text("source")

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.unique(["stock_id", "report_date", "report_type"])

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("balance_sheets")
