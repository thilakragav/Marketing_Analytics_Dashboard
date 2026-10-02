import os
from pathlib import Path
import pandas as pd
from typing import Optional
from app.services.data_sources.base import BaseDataSourceConnector

class CSVLoader(BaseDataSourceConnector):
    """Fallback loader reading raw and processed CSV marketing datasets."""
    def __init__(self, base_dir: Optional[Path] = None):
        super().__init__("Static CSV Loader")
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parents[3] / "data"
        else:
            self.base_dir = Path(base_dir)
        self.is_connected = True
        self.is_live = False

    def connect(self) -> bool:
        self.is_connected = self.base_dir.exists()
        return self.is_connected

    def fetch_data(self, dataset_name: str = "paid_media", start_date=None, end_date=None) -> Optional[pd.DataFrame]:
        mapping = {
            "paid_media": self.base_dir / "processed" / "unified_paid_media_daily.csv",
            "campaigns": self.base_dir / "processed" / "campaign_performance_summary.csv",
            "ga4": self.base_dir / "raw" / "ga4" / "ga4_daily_channel.csv",
            "gsc": self.base_dir / "raw" / "gsc" / "gsc_daily_queries.csv",
            "google_ads": self.base_dir / "raw" / "google_ads" / "daily_campaign_performance.csv",
            "meta": self.base_dir / "raw" / "meta" / "daily_campaign_performance.csv",
            "linkedin": self.base_dir / "raw" / "linkedin" / "daily_campaign_performance.csv",
        }
        target_path = mapping.get(dataset_name)
        if target_path and target_path.exists():
            df = pd.read_csv(target_path)
            self.record_count = len(df)
            return df
        self.error_message = f"CSV dataset {dataset_name} not found at {target_path}"
        return None

    def validate_data(self, df: pd.DataFrame) -> bool:
        return df is not None and not df.empty

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.date
        return df

    def load_to_database(self, df: pd.DataFrame, engine, table_name: str = "paid_media_daily") -> bool:
        try:
            df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=200)
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
