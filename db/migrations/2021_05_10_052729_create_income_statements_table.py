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
            table.date("fiscal_date")
            table.char("report_type", 2)

            table.text("currency")
            table.big_integer("total_revenue")
            table.big_integer("cost_of_revenue")
            table.big_integer("gross_profit")
            table.big_integer("operating_income")
            table.big_integer("income_before_tax")
            table.big_integer("income_tax")
            table.big_integer("net_income_from_operations")
            table.big_integer("net_income")

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.unique(["stock_id", "fiscal_date", "report_type"])

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("income_statements")
