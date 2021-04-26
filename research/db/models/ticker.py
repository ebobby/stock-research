from orator import Model


class Ticker(Model):
    """Ticker model."""

    @staticmethod
    def by_symbol_or_new(symbol):
        return Ticker.where("symbol", "=", symbol).first() or Ticker()
