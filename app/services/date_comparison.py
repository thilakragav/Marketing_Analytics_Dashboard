import pandas as pd
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

def get_comparison_date_range(
    start_date: date,
    end_date: date,
    comparison_mode: str = "Previous Period",
    custom_start: date = None,
    custom_end: date = None
) -> tuple[date, date, str]:
    """
    Computes comparison start and end dates based on the selected mode:
    - Previous Period: Exactly equal duration immediately preceding current start date.
    - Previous Month: 1 calendar month prior.
    - Previous Quarter: 3 months / 1 quarter prior.
    - Previous Year: 1 calendar year prior.
    - Custom: Custom selected start and end dates.
    """
    duration_days = (end_date - start_date).days + 1

    if comparison_mode == "Previous Month":
        comp_start = start_date - relativedelta(months=1)
        comp_end = end_date - relativedelta(months=1)
        label = "vs previous month"
    elif comparison_mode == "Previous Quarter":
        comp_start = start_date - relativedelta(months=3)
        comp_end = end_date - relativedelta(months=3)
        label = "vs previous quarter"
    elif comparison_mode == "Previous Year":
        comp_start = start_date - relativedelta(years=1)
        comp_end = end_date - relativedelta(years=1)
        label = "vs previous year"
    elif comparison_mode == "Custom" and custom_start and custom_end:
        comp_start = custom_start
        comp_end = custom_end
        label = f"vs custom ({custom_start} to {custom_end})"
    else:  # "Previous Period" default
        comp_end = start_date - timedelta(days=1)
        comp_start = comp_end - timedelta(days=duration_days - 1)
        label = "vs previous period"

    return comp_start, comp_end, label

def compute_metric_change(
    current_val: float,
    previous_val: float,
    higher_is_better: bool = True
) -> dict:
    """
    Calculates absolute change, percentage change, and trend direction.
    Safely handles zero/empty previous periods by returning 'N/A' or 'Insufficient Data'.
    """
    if current_val is None:
        current_val = 0.0
    if previous_val is None:
        previous_val = 0.0

    abs_change = current_val - previous_val

    if previous_val == 0 or pd.isna(previous_val):
        pct_change = None
        pct_change_str = "Insufficient Data" if current_val == 0 else "N/A"
    else:
        pct_change = (abs_change / abs(previous_val)) * 100.0
        sign = "+" if pct_change > 0 else ""
        pct_change_str = f"{sign}{pct_change:.2f}%"

    # Trend direction
    if abs(abs_change) < 1e-6:
        trend = "→ Flat"
        trend_status = "neutral"
    elif abs_change > 0:
        trend = "↑ Increasing"
        trend_status = "positive" if higher_is_better else "negative"
    else:
        trend = "↓ Decreasing"
        trend_status = "negative" if higher_is_better else "positive"

    return {
        "current": current_val,
        "previous": previous_val,
        "abs_change": abs_change,
        "pct_change": pct_change,
        "pct_change_str": pct_change_str,
        "trend": trend,
        "trend_status": trend_status,
        "higher_is_better": higher_is_better
    }

def check_incomplete_period(end_date: date, max_data_date: date) -> bool:
    """Returns True if the current period selection extends past available recorded dates."""
    if not max_data_date:
        return False
    return end_date > max_data_date
