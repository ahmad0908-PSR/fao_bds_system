"""
SQLAlchemy engine + session factory, shared by both applications.
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from shared.config import DATABASE_URL

# check_same_thread=False is required for SQLite when used from Streamlit,
# since Streamlit can touch the connection from different threads/reruns.
# This is a SQLite-only quirk — Postgres doesn't need or accept it, so we
# only pass it when DATABASE_URL is actually a SQLite URL.
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# pool_pre_ping avoids "server closed the connection" errors from hosted
# Postgres providers (e.g. Neon) that close idle connections after a
# period of inactivity — the pool checks the connection is alive before
# reusing it, and transparently reconnects if not.
engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


@contextmanager
def get_session():
    """
    Context-managed DB session.

    Usage:
        with get_session() as session:
            session.add(obj)
            session.commit()
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
