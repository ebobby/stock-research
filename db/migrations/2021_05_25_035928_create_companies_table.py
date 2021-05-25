from orator.migrations import Migration


class CreateCompaniesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("company_profiles") as table:
            table.big_increments("id")
            table.integer("stock_id").unsigned()

            table.text("name")
            table.text("description")
            table.text("address")
            table.text("phone")
            table.text("url")
            table.text("logo_url")

            table.text("exchange")
            table.text("currency")
            table.text("country")
            table.text("location")

            table.text("sector")
            table.text("industry")

            table.text("isin").nullable()
            table.text("cusip").nullable()
            table.text("cik").nullable()

            table.big_integer("fulltime_employees")
            table.decimal("market_capitalization", 20, 5)

            table.date("ipo_date").nullable()
            table.date("last_update_date").nullable()

            table.text("source")

            # Timestamps
            table.timestamps()

            # Indexes
            table.foreign("stock_id").references("id").on("stocks")
            table.unique("stock_id")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("company_profiles")
