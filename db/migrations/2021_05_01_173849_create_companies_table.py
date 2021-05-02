from orator.migrations import Migration


class CreateCompaniesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("companies") as table:
            table.increments("id")

            table.integer("stock_id").unsigned()
            table.foreign("stock_id").references("id").on("stocks")

            table.text("name").nullable()
            table.text("cik").nullable()
            table.text("description").nullable()
            table.text("address").nullable()
            table.text("country").nullable()
            table.text("currency").nullable()
            table.text("sector").nullable()
            table.text("industry").nullable()
            table.big_integer("fulltime_employees").nullable()

            table.index("stock_id")

            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("companies")
