import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
import tomllib

# Base paths
BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = PROCESSED_DIR / "global_geographic_sales.csv"

# Global country metadata with ISO-3, coordinates, and market distribution profiles
COUNTRY_PROFILES = [
    {"code": "USA", "name": "United States", "region": "North America", "flag": "🇺🇸", "lat": 37.0902, "lon": -95.7129, "share": 0.425, "aov": 159.2, "growth": 14.8},
    {"code": "GBR", "name": "United Kingdom", "region": "Europe", "flag": "🇬🇧", "lat": 55.3781, "lon": -3.4360, "share": 0.122, "aov": 158.5, "growth": 11.2},
    {"code": "IND", "name": "India", "region": "Asia-Pacific", "flag": "🇮🇳", "lat": 20.5937, "lon": 78.9629, "share": 0.108, "aov": 114.5, "growth": 28.4},
    {"code": "DEU", "name": "Germany", "region": "Europe", "flag": "🇩🇪", "lat": 51.1657, "lon": 10.4515, "share": 0.074, "aov": 162.0, "growth": 9.5},
    {"code": "CAN", "name": "Canada", "region": "North America", "flag": "🇨🇦", "lat": 56.1304, "lon": -106.3468, "share": 0.061, "aov": 160.8, "growth": 12.1},
    {"code": "AUS", "name": "Australia", "region": "Asia-Pacific", "flag": "🇦🇺", "lat": -25.2744, "lon": 133.7751, "share": 0.045, "aov": 165.4, "growth": 15.6},
    {"code": "FRA", "name": "France", "region": "Europe", "flag": "🇫🇷", "lat": 46.2276, "lon": 2.2137, "share": 0.038, "aov": 155.0, "growth": 8.7},
    {"code": "JPN", "name": "Japan", "region": "Asia-Pacific", "flag": "🇯🇵", "lat": 36.2048, "lon": 138.2529, "share": 0.032, "aov": 168.0, "growth": 7.3},
    {"code": "NLD", "name": "Netherlands", "region": "Europe", "flag": "🇳🇱", "lat": 52.1326, "lon": 5.2913, "share": 0.019, "aov": 157.2, "growth": 13.9},
    {"code": "SGP", "name": "Singapore", "region": "Asia-Pacific", "flag": "🇸🇬", "lat": 1.3521, "lon": 103.8198, "share": 0.016, "aov": 172.5, "growth": 21.0},
    {"code": "BRA", "name": "Brazil", "region": "Latin America", "flag": "🇧🇷", "lat": -14.2350, "lon": -51.9253, "share": 0.015, "aov": 146.0, "growth": 19.4},
    {"code": "ARE", "name": "United Arab Emirates", "region": "Middle East & Africa", "flag": "🇦🇪", "lat": 23.4241, "lon": 53.8478, "share": 0.013, "aov": 182.0, "growth": 24.5},
    {"code": "ITA", "name": "Italy", "region": "Europe", "flag": "🇮🇹", "lat": 41.8719, "lon": 12.5674, "share": 0.011, "aov": 151.0, "growth": 6.8},
    {"code": "ESP", "name": "Spain", "region": "Europe", "flag": "🇪🇸", "lat": 40.4637, "lon": -3.7492, "share": 0.009, "aov": 149.5, "growth": 10.3},
    {"code": "CHE", "name": "Switzerland", "region": "Europe", "flag": "🇨🇭", "lat": 46.8182, "lon": 8.2275, "share": 0.008, "aov": 188.0, "growth": 8.1},
    {"code": "MEX", "name": "Mexico", "region": "Latin America", "flag": "🇲🇽", "lat": 23.6345, "lon": -102.5528, "share": 0.007, "aov": 141.0, "growth": 16.7},
    {"code": "SWE", "name": "Sweden", "region": "Europe", "flag": "🇸🇪", "lat": 60.1282, "lon": 18.6435, "share": 0.006, "aov": 164.0, "growth": 11.0},
    {"code": "KOR", "name": "South Korea", "region": "Asia-Pacific", "flag": "🇰🇷", "lat": 35.9078, "lon": 127.7669, "share": 0.005, "aov": 158.0, "growth": 13.5},
    {"code": "SAU", "name": "Saudi Arabia", "region": "Middle East & Africa", "flag": "🇸🇦", "lat": 23.8859, "lon": 45.0792, "share": 0.005, "aov": 175.0, "growth": 22.8},
    {"code": "ZAF", "name": "South Africa", "region": "Middle East & Africa", "flag": "🇿🇦", "lat": -30.5595, "lon": 22.9375, "share": 0.004, "aov": 139.0, "growth": 14.1},
    {"code": "IRL", "name": "Ireland", "region": "Europe", "flag": "🇮🇪", "lat": 53.1424, "lon": -7.6921, "share": 0.004, "aov": 163.0, "growth": 12.4},
    {"code": "NZL", "name": "New Zealand", "region": "Asia-Pacific", "flag": "🇳🇿", "lat": -40.9006, "lon": 174.8860, "share": 0.003, "aov": 161.0, "growth": 10.9},
    {"code": "BEL", "name": "Belgium", "region": "Europe", "flag": "🇧🇪", "lat": 50.5039, "lon": 4.4699, "share": 0.003, "aov": 154.0, "growth": 7.9},
    {"code": "NOR", "name": "Norway", "region": "Europe", "flag": "🇳🇴", "lat": 60.4720, "lon": 8.4689, "share": 0.003, "aov": 171.0, "growth": 9.2},
    {"code": "POL", "name": "Poland", "region": "Europe", "flag": "🇵🇱", "lat": 51.9194, "lon": 19.1451, "share": 0.002, "aov": 142.0, "growth": 17.5},
    {"code": "DNK", "name": "Denmark", "region": "Europe", "flag": "🇩🇰", "lat": 56.2639, "lon": 9.5018, "share": 0.002, "aov": 166.0, "growth": 8.4},
    {"code": "ISR", "name": "Israel", "region": "Middle East & Africa", "flag": "🇮🇱", "lat": 31.0461, "lon": 34.8516, "share": 0.002, "aov": 168.0, "growth": 15.0},
    {"code": "ARG", "name": "Argentina", "region": "Latin America", "flag": "🇦🇷", "lat": -38.4161, "lon": -63.6167, "share": 0.0015, "aov": 138.0, "growth": 18.2},
    {"code": "CHL", "name": "Chile", "region": "Latin America", "flag": "🇨🇱", "lat": -35.6751, "lon": -71.5430, "share": 0.0015, "aov": 144.0, "growth": 14.3},
    {"code": "MYS", "name": "Malaysia", "region": "Asia-Pacific", "flag": "🇲🇾", "lat": 4.2105, "lon": 101.9758, "share": 0.0015, "aov": 136.0, "growth": 20.1},
    {"code": "IDN", "name": "Indonesia", "region": "Asia-Pacific", "flag": "🇮🇩", "lat": -0.7893, "lon": 113.9213, "share": 0.0015, "aov": 128.0, "growth": 25.6},
    {"code": "PHL", "name": "Philippines", "region": "Asia-Pacific", "flag": "🇵🇭", "lat": 12.8797, "lon": 121.7740, "share": 0.0015, "aov": 131.0, "growth": 23.0},
]

def generate_geo_data():
    # Target totals matching paid media / marketing suite
    TOTAL_REVENUE_USD = 50971790.83
    TOTAL_SPEND_USD = 2460157.96

    rows = []
    # Normalize shares to exactly 1.0
    total_share = sum(p["share"] for p in COUNTRY_PROFILES)
    for p in COUNTRY_PROFILES:
        norm_share = p["share"] / total_share
        sales_usd = round(TOTAL_REVENUE_USD * norm_share, 2)
        spend_usd = round(TOTAL_SPEND_USD * norm_share, 2)
        aov = p["aov"]
        orders = int(round(sales_usd / aov))
        roas = round(sales_usd / spend_usd, 2) if spend_usd > 0 else 0.0

        rows.append({
            "country_code": p["code"],
            "country_name": p["name"],
            "region": p["region"],
            "flag": p["flag"],
            "latitude": p["lat"],
            "longitude": p["lon"],
            "sales_revenue_usd": sales_usd,
            "orders_count": orders,
            "ad_spend_usd": spend_usd,
            "aov_usd": round(sales_usd / orders, 2) if orders > 0 else aov,
            "roas": roas,
            "market_share_pct": round(norm_share * 100, 2),
            "growth_rate_pct": p["growth"],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(rows)
    # Save CSV
    df.to_csv(CSV_FILE, index=False)
    print(f"Saved {len(df)} country records to {CSV_FILE}")

    # Load into PostgreSQL
    try:
        secrets_path = BASE_DIR / ".streamlit" / "secrets.toml"
        if secrets_path.exists():
            with open(secrets_path, "rb") as f:
                sec = tomllib.load(f)
            pw = quote_plus(sec.get("DB_PASSWORD", ""))
            engine = create_engine(f"postgresql+psycopg2://postgres:{pw}@127.0.0.1:5432/marketing_dashboard")

            with engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS global_geographic_sales CASCADE;"))
                conn.commit()

            df.to_sql("global_geographic_sales", engine, if_exists="replace", index=False)
            print("Successfully populated 'global_geographic_sales' in PostgreSQL database.")
    except Exception as e:
        print(f"Notice: PostgreSQL sync: {e}")

if __name__ == "__main__":
    generate_geo_data()
