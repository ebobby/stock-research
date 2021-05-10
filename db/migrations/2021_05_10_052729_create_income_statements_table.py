from orator.migrations import Migration


class CreateIncomeStatementsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("income_statements") as table:
            table.big_increments("id")

            table.integer("stock_id").unsigned()

            # Data
            table.date("report_date")
            table.char("report_type", 2)

            table.text("currency").nullable()
            table.decimal("total_revenue", 20, 5)
            table.decimal("cost_of_revenue", 20, 5)
            table.decimal("gross_profit", 20, 5)

            table.decimal("sga_expense", 20, 5)
            table.decimal("research_and_development", 20, 5)
            table.decimal("depreciation_and_amortization", 20, 5)

            table.decimal("operating_expenses", 20, 5)
            table.decimal("operating_income", 20, 5)

            table.decimal("interest_expense", 20, 5)
            table.decimal("interest_income", 20, 5)
            table.decimal("total_other_income_expenses", 20, 5)

            table.decimal("income_before_tax", 20, 5)
            table.decimal("income_tax_expense", 20, 5)
            table.decimal("net_income_after_tax", 20, 5)
            table.decimal("discontinued_operations", 20, 5)
            table.decimal("net_income", 20, 5)

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
        self.schema.drop("income_statements")
