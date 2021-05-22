from orator.migrations import Migration


class CreateCashFlowStatementsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("cash_flow_statements") as table:
            table.big_increments("id")

            table.integer("stock_id").unsigned()

            # Data
            table.date("report_date")
            table.char("report_type", 2)
            table.text("currency").nullable()

            table.decimal("net_income", 20, 5)
            table.decimal("depreciation", 20, 5)
            table.decimal("other_cash_from_operating_activites", 20, 5)
            table.decimal("total_cash_from_operating_activities", 20, 5)
            table.decimal("capital_expenditures", 20, 5)
            table.decimal("investments", 20, 5)
            table.decimal("other_cash_from_investing_activities", 20, 5)
            table.decimal("total_cash_from_investing_activities", 20, 5)
            table.decimal("net_borrowing", 20, 5)
            table.decimal("dividends_paid", 20, 5)
            table.decimal("sale_or_purchase_of_stock", 20, 5)
            table.decimal("other_cash_from_financing_activities", 20, 5)
            table.decimal("total_cash_from_financing_activities", 20, 5)
            table.decimal("initial_cash", 20, 5)
            table.decimal("change_in_cash", 20, 5)
            table.decimal("final_cash", 20, 5)
            table.decimal("free_cash_flow", 20, 5)
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
        self.schema.drop("cash_flow_statements")
