from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

GSC_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "gsc"
    / "gsc_daily_queries.csv"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_USER = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "marketing_dashboard"

DB_PASSWORD = getpass("Enter PostgreSQL password: ")


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:"
    f"{quote_plus(DB_PASSWORD)}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ============================================================
# VALIDATE SOURCE FILE
# ============================================================

if not GSC_FILE.exists():
    raise FileNotFoundError(
        f"GSC CSV not found:\n{GSC_FILE}"
    )

print(f"\nGSC file found:")
print(GSC_FILE)


# ============================================================
# LOAD CSV
# ============================================================

df = pd.read_csv(GSC_FILE)

print(f"\nRows read: {len(df):,}")
print(f"Columns: {list(df.columns)}")


# ============================================================
# VALIDATE EXPECTED COLUMNS
# ============================================================

EXPECTED_COLUMNS = [
    "date",
    "query",
    "page",
    "country",
    "device",
    "search_type",
    "query_type",
    "clicks",
    "impressions",
    "ctr",
    "average_position",
]

missing_columns = [
    column
    for column in EXPECTED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing expected GSC columns: {missing_columns}"
    )

df = df[EXPECTED_COLUMNS].copy()


# ============================================================
# DATA TYPES
# ============================================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
).dt.date

for column in [
    "clicks",
    "impressions",
]:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0).astype(int)

for column in [
    "ctr",
    "average_position",
]:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


# ============================================================
# BASIC DATA VALIDATION
# ============================================================

if df["date"].isna().any():
    raise ValueError("Some rows contain invalid dates.")

if df["query"].isna().any():
    raise ValueError("Some rows contain missing queries.")

print("\nData validation passed.")


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

with engine.connect() as connection:
    database_name = connection.execute(
        text("SELECT current_database()")
    ).scalar()

    print(f"Connected to PostgreSQL database: {database_name}")

    if database_name != DB_NAME:
        raise RuntimeError(
            f"Connected to '{database_name}', "
            f"but expected '{DB_NAME}'."
        )


# ============================================================
# LOAD INTO POSTGRESQL
# ============================================================

TABLE_NAME = "gsc_daily_queries"

df.to_sql(
    TABLE_NAME,
    engine,
    if_exists="replace",
    index=False,
    method="multi",
    chunksize=1000
)

print(
    f"\nSuccessfully loaded {len(df):,} rows "
    f"into '{TABLE_NAME}'."
)


# ============================================================
# VERIFY DATABASE TABLE
# ============================================================

with engine.connect() as connection:
    row_count = connection.execute(
        text(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    ).scalar()

    print(
        f"PostgreSQL verification: "
        f"{row_count:,} rows in {TABLE_NAME}"
    )

    if row_count != len(df):
        raise RuntimeError(
            f"Row-count mismatch: CSV={len(df):,}, "
            f"PostgreSQL={row_count:,}"
        )

print("\nGSC ingestion completed successfully.")