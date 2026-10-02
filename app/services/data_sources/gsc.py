import os
import streamlit as st
import pandas as pd
from typing import Optional
from app.services.data_sources.base import BaseDataSourceConnector
from app.services.data_sources.csv_loader import CSVLoader

class GSCConnector(BaseDataSourceConnector):
    """
    Google Search Console Search Analytics API connector.
    Reads credentials from os.environ or st.secrets['GSC_PROPERTY'].
    Gracefully falls back to Static CSV / PostgreSQL when credentials are not configured.
    """
    def __init__(self):
        super().__init__("Google Search Console")
        self.property_url = os.getenv("GSC_PROPERTY") or st.secrets.get("GSC_PROPERTY")
        self.csv_fallback = CSVLoader()

    def connect(self) -> bool:
        if self.property_url:
            self.is_connected = True
            self.is_live = True
            return True
        else:
            self.is_connected = self.csv_fallback.connect()
            self.is_live = False
            return self.is_connected

    def fetch_data(self, start_date=None, end_date=None) -> Optional[pd.DataFrame]:
        return self.csv_fallback.fetch_data("gsc", start_date, end_date)

    def validate_data(self, df: pd.DataFrame) -> bool:
        required = ["date", "query", "clicks", "impressions", "ctr", "average_position"]
        return df is not None and all(col in df.columns for col in required)

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.csv_fallback.normalize_data(df)

    def load_to_database(self, df: pd.DataFrame, engine) -> bool:
        return self.csv_fallback.load_to_database(df, engine, "gsc_daily_queries")
