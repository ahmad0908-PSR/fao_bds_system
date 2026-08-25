"""
Run this once to create the SQLite database and the businesses table.

Usage (from the project root, with your venv active):
    python -m shared.database.init_db
"""

from shared.database.engine import engine, Base
from shared.database import models  # noqa: F401  (import registers the model with Base)


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
    print(f"Tables created: {list(Base.metadata.tables.keys())}")


if __name__ == "__main__":
    init_db()
