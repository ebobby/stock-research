from orator.migrations import Migration


class CreateStocksTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("stocks") as table:
            table.increments("id")

            # Data
            table.text("symbol")
            table.text("name")
            table.text("country")
            table.text("currency")
            table.text("exchange")
            table.boolean("active")

            # Timestamps
            table.timestamps()

            # Indexes
            table.unique("symbol")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("stocks")
