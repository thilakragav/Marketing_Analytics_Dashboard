import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os


# --------------------------------------------------
# DATABASE CONFIG
# --------------------------------------------------

DB_USER = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "marketing_dashboard"

DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    DB_PASSWORD = input("Enter PostgreSQL password: ")


DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:"
    f"{quote_plus(DB_PASSWORD)}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# --------------------------------------------------
# FILE PATH
# --------------------------------------------------

CSV_PATH = "data/raw/ga4/ga4_daily_channel.csv"


# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

print("Reading GA4 CSV...")

df = pd.read_csv(CSV_PATH)

print(f"Rows loaded from CSV: {len(df):,}")

print("\nColumns:")
print(df.columns.tolist())


# --------------------------------------------------
# DATA TYPES
# --------------------------------------------------

df["date"] = pd.to_datetime(
    df["date"]
).dt.date

df["source_refresh_timestamp"] = pd.to_datetime(
    df["source_refresh_timestamp"]
)

numeric_columns = [
    "users",
    "new_users",
    "sessions",
    "engaged_sessions",
    "engagement_rate",
    "conversions",
    "revenue"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# BASIC VALIDATION
# --------------------------------------------------

print("\nRunning validation...")

print(
    "Missing values:",
    df.isnull().sum().sum()
)

print(
    "Duplicate rows:",
    df.duplicated().sum()
)

print(
    "Date range:",
    df["date"].min(),
    "to",
    df["date"].max()
)


# --------------------------------------------------
# LOAD INTO POSTGRESQL
# --------------------------------------------------

print("\nLoading GA4 data into PostgreSQL...")

with engine.begin() as connection:

    connection.execute(
        text(
            "TRUNCATE TABLE ga4_daily_channel"
        )
    )

df.to_sql(
    "ga4_daily_channel",
    engine,
    if_exists="append",
    index=False,
    chunksize=100
)


# --------------------------------------------------
# VERIFY
# --------------------------------------------------

with engine.connect() as connection:

    result = connection.execute(
        text(
            "SELECT COUNT(*) "
            "FROM ga4_daily_channel"
        )
    )

    row_count = result.scalar()


print("\n----------------------------------")
print("GA4 LOAD COMPLETE ✅")
print("----------------------------------")

print(
    f"ga4_daily_channel : {row_count:,} rows"
)

print("----------------------------------")