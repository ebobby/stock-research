from orator.migrations import Migration


class StockDiscountedCashFlows(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("discounted_cash_flows") as table:
            table.big_increments("id")
            table.integer("stock_id").unsigned()
            table.date("last_date")
            table.text("symbol")
            table.decimal("discount_rate", 20, 5)
            table.decimal("discounted_cash_flows", 25, 5)
            table.decimal("discounted_share_price", 20, 5)

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.unique("stock_id")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("discounted_cash_flows")
