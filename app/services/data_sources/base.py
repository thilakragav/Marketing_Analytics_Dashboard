from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, Any

class BaseDataSourceConnector(ABC):
    """
    Abstract Base Class for marketing data connectors.
    Provides standard lifecycle methods:
    connect() -> fetch_data() -> validate_data() -> normalize_data() -> load_to_database()
    """
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.is_connected = False
        self.is_live = False
        self.last_refresh = None
        self.record_count = 0
        self.error_message: Optional[str] = None

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to live API or fallback data source."""
        pass

    @abstractmethod
    def fetch_data(self, start_date=None, end_date=None) -> Optional[pd.DataFrame]:
        """Fetch raw payload from API endpoint or static repository."""
        pass

    @abstractmethod
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate presence of mandatory columns, data types, and null constraints."""
        pass

    @abstractmethod
    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names, dates, metrics, and data types."""
        pass

    @abstractmethod
    def load_to_database(self, df: pd.DataFrame, engine) -> bool:
        """Persist normalized dataset into analytical PostgreSQL tables."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Return real-time diagnostic status of the connector."""
        return {
            "source_name": self.source_name,
            "is_connected": self.is_connected,
            "source_type": "Live API" if self.is_live else "Static CSV / PostgreSQL",
            "status": "Fresh" if self.is_connected and not self.error_message else ("Failed" if self.error_message else "Unavailable"),
            "last_refresh": self.last_refresh,
            "record_count": self.record_count,
            "error_message": self.error_message
        }
