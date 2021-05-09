from orator.migrations import Migration


class CreateStocksTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("stocks") as table:
            table.increments("id")

            # Data
            table.text("ticker")
            table.text("name")
            table.text("locale")
            table.text("currency")
            table.text("exchange")
            table.text("cik")
            table.boolean("active")

            # Timestamps
            table.timestamps()

            # Indexes
            table.unique("ticker")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("stocks")
