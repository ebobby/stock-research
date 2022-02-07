from orator import DatabaseManager, Model

config = {
    "stock-research": {
        "driver": "postgres",
        "host": "localhost",
        "database": "stock-research",
        "user": "stocks",
        "password": "stocks",
        "prefix": "",
        "log_queries": True,
    }
}

db = DatabaseManager(config)

Model.set_connection_resolver(db)
