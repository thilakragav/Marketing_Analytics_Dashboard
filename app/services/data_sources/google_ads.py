import os
import streamlit as st
import pandas as pd
from typing import Optional
from app.services.data_sources.base import BaseDataSourceConnector
from app.services.data_sources.csv_loader import CSVLoader

class GoogleAdsConnector(BaseDataSourceConnector):
    """
    Google Ads API connector.
    Reads credentials from os.environ or st.secrets:
    - GOOGLE_ADS_CUSTOMER_ID
    - GOOGLE_ADS_DEVELOPER_TOKEN
    Gracefully falls back to Static CSV / PostgreSQL when credentials are not configured.
    """
    def __init__(self):
        super().__init__("Google Ads")
        self.customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID") or st.secrets.get("GOOGLE_ADS_CUSTOMER_ID")
        self.developer_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN") or st.secrets.get("GOOGLE_ADS_DEVELOPER_TOKEN")
        self.csv_fallback = CSVLoader()

    def connect(self) -> bool:
        if self.customer_id and self.developer_token:
            self.is_connected = True
            self.is_live = True
            return True
        else:
            self.is_connected = self.csv_fallback.connect()
            self.is_live = False
            return self.is_connected

    def fetch_data(self, start_date=None, end_date=None) -> Optional[pd.DataFrame]:
        return self.csv_fallback.fetch_data("google_ads", start_date, end_date)

    def validate_data(self, df: pd.DataFrame) -> bool:
        required = ["date", "campaign_name", "spend", "clicks", "conversions"]
        return df is not None and all(col in df.columns for col in required)

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.csv_fallback.normalize_data(df)

    def load_to_database(self, df: pd.DataFrame, engine) -> bool:
        return self.csv_fallback.load_to_database(df, engine, "paid_media_daily")
