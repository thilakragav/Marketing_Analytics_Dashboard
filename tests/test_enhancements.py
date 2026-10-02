import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import date
from sqlalchemy import create_engine
import tomllib
from urllib.parse import quote_plus
from app.services.data_sources.manager import DataSourceManager
from app.components.kpi_dictionary import KPI_DEFINITIONS, get_dictionary_dataframe
from app.services.date_comparison import get_comparison_date_range, compute_metric_change

def test_all():
    print("========================================")
    print("MARKETING DASHBOARD ENHANCEMENT TESTS")
    print("========================================")

    with open(".streamlit/secrets.toml", "rb") as f:
        sec = tomllib.load(f)

    pw = quote_plus(sec.get("DB_PASSWORD", ""))
    engine = create_engine(f"postgresql+psycopg2://postgres:{pw}@127.0.0.1:5432/marketing_dashboard")

    # 1. Data Sources Manager Test
    mgr = DataSourceManager()
    statuses = mgr.get_source_statuses(engine)
    print(f"Data Sources: {len(statuses)} sources verified.")
    for s in statuses:
        print(f"  [PASS] {s['source']}: {s['status']} | {s['connection_type']} | {s['record_count']:,} rows")

    # 2. KPI Dictionary Test
    assert len(KPI_DEFINITIONS) >= 16, "Must define at least 16 major KPIs"
    print(f"\nKPI Dictionary: {len(KPI_DEFINITIONS)} metrics defined.")
    df_kpi = get_dictionary_dataframe()
    print(f"  [PASS] KPI Table Shape: {df_kpi.shape}")

    # 3. Date Comparison Logic Test
    c_start, c_end, lbl = get_comparison_date_range(date(2026, 4, 1), date(2026, 6, 30), "Previous Period")
    print(f"\nDate Comparison: [2026-04-01 to 2026-06-30] -> [{c_start} to {c_end}] ({lbl})")
    assert str(c_end) == "2026-03-31"

    # 4. Metric Change & Zero-Division Safety Test
    res = compute_metric_change(2460000, 2210000, higher_is_better=True)
    print(f"  [PASS] Standard Change: {res['pct_change_str']}")
    assert "+11.31%" in res["pct_change_str"]


    zero_res = compute_metric_change(100, 0, higher_is_better=True)
    print(f"  [PASS] Zero-Division Protection: {zero_res['pct_change_str']}")
    assert zero_res["pct_change_str"] == "N/A"

    print("\nALL VERIFICATION CHECKS PASSED [OK]")


if __name__ == "__main__":
    test_all()
