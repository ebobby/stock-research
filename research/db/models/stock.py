from orator import Model, SoftDeletes


class Stock(SoftDeletes, Model):
    """Stock/Shares."""

    __dates__ = ["deleted_at"]

    @staticmethod
    def by_symbol_or_new(symbol):
        return Stock.where("symbol", "=", symbol).first() or Stock()
