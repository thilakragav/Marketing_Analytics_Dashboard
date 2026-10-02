import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def get_engine():
    """Create PostgreSQL SQLAlchemy engine safely."""

    db_user = st.secrets.get("DB_USER", "postgres")
    db_password = st.secrets.get("DB_PASSWORD", "Thilak@2005")
    db_host = st.secrets.get("DB_HOST", "127.0.0.1")
    db_port = st.secrets.get("DB_PORT", "5432")
    db_name = st.secrets.get("DB_NAME", "marketing_dashboard")

    if not db_password:
        raise ValueError(
            "DB_PASSWORD is not configured in .streamlit/secrets.toml"
        )

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=int(db_port),
        database=db_name,
    )

    return create_engine(connection_url)


def run_query(query: str) -> pd.DataFrame:
    """Execute a SQL query and return the result as a DataFrame."""

    engine = get_engine()

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)