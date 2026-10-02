from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_USER = "postgres"
DB_PASSWORD = input("Enter PostgreSQL password: ")
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "marketing_dashboard"


# ============================================================
# ENCODE PASSWORD FOR DATABASE URL
# ============================================================

# Important:
# Special characters such as @, :, /, #, etc.
# must be URL-encoded when used inside a database URL.

ENCODED_PASSWORD = quote_plus(DB_PASSWORD)


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{ENCODED_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ============================================================
# CREATE DATABASE ENGINE
# ============================================================

print("=" * 70)
print("POSTGRESQL DATA LOADER")
print("=" * 70)

print("\nConnecting to PostgreSQL...")

engine = create_engine(DATABASE_URL)


# ============================================================
# TEST CONNECTION
# ============================================================

try:

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database();")
        )

        database_name = result.scalar()

        print(f"Connected to database: {database_name}")
        print("Connection successful ✅")


except Exception as error:

    print("\nDatabase connection failed ❌")
    print(error)

    raise SystemExit(1)


# ============================================================
# LOAD DAILY PAID MEDIA
# ============================================================

daily_file = (
    PROCESSED_DIR /
    "unified_paid_media_daily.csv"
)

print("\nLoading daily paid media data...")

daily_df = pd.read_csv(daily_file)

print(f"Rows found: {len(daily_df):,}")


# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

daily_df["date"] = pd.to_datetime(
    daily_df["date"]
)

daily_df["source_refresh_timestamp"] = pd.to_datetime(
    daily_df["source_refresh_timestamp"]
)

daily_df["start_date"] = pd.to_datetime(
    daily_df["start_date"]
)

daily_df["end_date"] = pd.to_datetime(
    daily_df["end_date"]
)


# ============================================================
# INSERT DAILY DATA
# ============================================================

daily_df.to_sql(
    "paid_media_daily",
    engine,
    if_exists="replace",
    index=False,
    chunksize=100
)

print(
    f"Loaded {len(daily_df):,} rows "
    "into paid_media_daily ✅"
)


# ============================================================
# LOAD CAMPAIGN PERFORMANCE
# ============================================================

campaign_file = (
    PROCESSED_DIR /
    "campaign_performance_summary.csv"
)

print("\nLoading campaign performance...")

campaign_df = pd.read_csv(campaign_file)

print(f"Rows found: {len(campaign_df):,}")


# ============================================================
# INSERT CAMPAIGN DATA
# ============================================================

campaign_df.to_sql(
    "campaign_performance",
    engine,
    if_exists="replace",
    index=False,
    chunksize=100
)

print(
    f"Loaded {len(campaign_df):,} rows "
    "into campaign_performance ✅"
)


# ============================================================
# VERIFY ROW COUNTS
# ============================================================

print("\nVerifying database row counts...")

with engine.connect() as connection:

    daily_count = connection.execute(
        text(
            "SELECT COUNT(*) FROM paid_media_daily"
        )
    ).scalar()

    campaign_count = connection.execute(
        text(
            "SELECT COUNT(*) FROM campaign_performance"
        )
    ).scalar()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("LOAD SUMMARY")
print("=" * 70)

print(
    f"paid_media_daily       : "
    f"{daily_count:,} rows"
)

print(
    f"campaign_performance   : "
    f"{campaign_count:,} rows"
)

print("=" * 70)
print("DATABASE LOAD COMPLETE ✅")
print("=" * 70)