from __future__ import annotations

import os
from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine

DEFAULT_SCHEMAS = ("raw", "clean", "enriched")


def _build_uri() -> str:
    """Resolve the SQLAlchemy connection URI from the environment."""
    uri = os.getenv("STOCK_DB_URI")
    if uri:
        return uri

    host = os.getenv("STOCK_DB_HOST", "stockdb")
    port = os.getenv("STOCK_DB_PORT", "5432")
    user = os.getenv("STOCK_DB_USER", "stock")
    password = os.getenv("STOCK_DB_PASSWORD", "stock")
    name = os.getenv("STOCK_DB_NAME", "stocks")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def test_connection() -> None:
    """Raise if the database is unreachable. Used as the DAG's fail-fast pre-check."""
    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))


def init_schemas(schemas: tuple[str, ...] = DEFAULT_SCHEMAS) -> None:
    """Create the raw/clean/enriched schemas if they don't already exist.

    Schema names are fixed constants here (not user input), so the f-string is
    safe — never interpolate untrusted identifiers this way.
    """
    with get_connection() as conn:
        for schema in schemas:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))


def read_sql(query: str, params: dict | None = None) -> pd.DataFrame:
    """Run a parameterized SELECT and return the result as a DataFrame."""
    with get_engine().connect() as conn:
        return pd.read_sql(text(query), conn, params=params)


def write_dataframe(
    df: pd.DataFrame,
    table: str,
    schema: str = "raw",
    if_exists: str = "append",
    index: bool = False,
) -> int:
    """Write a DataFrame to <schema>.<table>; returns the number of rows written."""
    with get_engine().begin() as conn:
        df.to_sql(table, conn, schema=schema, if_exists=if_exists, index=index)
    return len(df)
