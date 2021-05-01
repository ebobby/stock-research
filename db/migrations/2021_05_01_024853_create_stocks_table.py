from orator.migrations import Migration


class CreateStocksTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("stocks") as table:
            table.increments("id")
            table.text("symbol")
            table.text("name")
            table.soft_deletes()
            table.timestamps()

            table.unique("symbol")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("stocks")
