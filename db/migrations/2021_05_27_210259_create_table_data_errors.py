from orator.migrations import Migration


class CreateTableDataErrors(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("errors") as table:
            table.big_increments("id")
            table.integer("stock_id").unsigned()

            table.text("message")
            table.text("source")

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.index("stock_id")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("errors")
