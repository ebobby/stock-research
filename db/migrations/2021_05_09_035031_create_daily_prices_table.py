from orator.migrations import Migration


class CreateDailyPricesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("daily_prices") as table:
            table.big_increments("id")

            table.integer("stock_id").unsigned()

            table.date("date")
            # Data
            table.decimal("open", 20, 4)
            table.decimal("high", 20, 4)
            table.decimal("low", 20, 4)
            table.decimal("close", 20, 4)
            table.decimal("adjusted_close", 20, 4)
            table.big_integer("volume")
            table.decimal("dividends", 20, 4).default(0.0)
            table.decimal("split_coefficient", 20, 4).default(1.0)

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.index("date")
            table.unique(["stock_id", "date"])

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("daily_prices")
