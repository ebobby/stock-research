from orator import DatabaseManager
from orator import Model

config = {
    "stock-research": {
        "driver": "postgres",
        "host": "localhost",
        "database": "stock-research",
        "user": "stocks",
        "password": "research",
        "prefix": "",
    }
}

db = DatabaseManager(config)

Model.set_connection_resolver(db)
