from orator import Model, SoftDeletes


class Etf(SoftDeletes, Model):
    """Exchange Traded Funds."""

    __dates__ = ["deleted_at"]

    @staticmethod
    def by_symbol_or_new(symbol):
        return Etf.where("symbol", "=", symbol).first() or Etf()
