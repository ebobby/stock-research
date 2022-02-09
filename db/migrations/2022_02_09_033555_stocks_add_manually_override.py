from orator.migrations import Migration


class StocksAddManuallyOverride(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("stocks") as table:
            table.boolean("force_inactive").default(False)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("stocks") as table:
            table.drop_column("force_inactive")
