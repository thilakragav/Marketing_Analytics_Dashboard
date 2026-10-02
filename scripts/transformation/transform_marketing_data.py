from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FILE PATHS
# ============================================================

GOOGLE_ADS_FILE = RAW_DIR / "google_ads" / "daily_campaign_performance.csv"
META_FILE = RAW_DIR / "meta" / "daily_campaign_performance.csv"
LINKEDIN_FILE = RAW_DIR / "linkedin" / "daily_campaign_performance.csv"

BUDGET_FILE = SYNTHETIC_DIR / "campaign_budget.csv"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_divide(numerator, denominator):
    """
    Safely divide two values.
    Returns NaN when denominator is zero.
    """
    return np.where(
        denominator != 0,
        numerator / denominator,
        np.nan
    )


# ============================================================
# 1. LOAD PAID MEDIA DATA
# ============================================================

print("=" * 70)
print("MARKETING PERFORMANCE DATA TRANSFORMATION")
print("=" * 70)

print("\nLoading paid media datasets...")

google_ads = pd.read_csv(GOOGLE_ADS_FILE)
meta_ads = pd.read_csv(META_FILE)
linkedin_ads = pd.read_csv(LINKEDIN_FILE)

print(f"Google Ads   : {len(google_ads):,} rows")
print(f"Meta Ads     : {len(meta_ads):,} rows")
print(f"LinkedIn Ads: {len(linkedin_ads):,} rows")


# ============================================================
# 2. COMBINE PAID MEDIA DATA
# ============================================================

print("\nCombining paid media datasets...")

paid_media = pd.concat(
    [
        google_ads,
        meta_ads,
        linkedin_ads
    ],
    ignore_index=True
)

print(f"Combined rows: {len(paid_media):,}")


# ============================================================
# 3. STANDARDIZE DATA TYPES
# ============================================================

print("\nStandardizing data types...")

paid_media["date"] = pd.to_datetime(
    paid_media["date"],
    errors="coerce"
)

paid_media["source_refresh_timestamp"] = pd.to_datetime(
    paid_media["source_refresh_timestamp"],
    errors="coerce"
)

numeric_columns = [
    "spend",
    "impressions",
    "reach",
    "clicks",
    "leads",
    "conversions",
    "conversion_value"
]

for column in numeric_columns:
    paid_media[column] = pd.to_numeric(
        paid_media[column],
        errors="coerce"
    ).fillna(0)


# ============================================================
# 4. STANDARDIZE TEXT COLUMNS
# ============================================================

text_columns = [
    "campaign_id",
    "platform",
    "account_id",
    "campaign_name",
    "objective",
    "currency"
]

for column in text_columns:
    paid_media[column] = (
        paid_media[column]
        .astype(str)
        .str.strip()
    )


# ============================================================
# 5. REMOVE DUPLICATES
# ============================================================

before_duplicates = len(paid_media)

paid_media = paid_media.drop_duplicates(
    subset=[
        "date",
        "campaign_id",
        "platform"
    ]
)

after_duplicates = len(paid_media)

print(
    f"Duplicates removed: "
    f"{before_duplicates - after_duplicates}"
)


# ============================================================
# 6. CALCULATE MARKETING KPIs
# ============================================================

print("\nCalculating marketing KPIs...")

# CTR
paid_media["ctr"] = safe_divide(
    paid_media["clicks"],
    paid_media["impressions"]
) * 100

# CPC
paid_media["cpc"] = safe_divide(
    paid_media["spend"],
    paid_media["clicks"]
)

# CPM
paid_media["cpm"] = safe_divide(
    paid_media["spend"],
    paid_media["impressions"]
) * 1000

# Conversion Rate
paid_media["conversion_rate"] = safe_divide(
    paid_media["conversions"],
    paid_media["clicks"]
) * 100

# CPA
paid_media["cpa"] = safe_divide(
    paid_media["spend"],
    paid_media["conversions"]
)

# CPL
paid_media["cpl"] = safe_divide(
    paid_media["spend"],
    paid_media["leads"]
)

# ROAS
paid_media["roas"] = safe_divide(
    paid_media["conversion_value"],
    paid_media["spend"]
)

# ROI
paid_media["roi"] = safe_divide(
    paid_media["conversion_value"] - paid_media["spend"],
    paid_media["spend"]
) * 100


# ============================================================
# 7. LOAD CAMPAIGN BUDGET
# ============================================================

print("\nLoading campaign budget...")

budget = pd.read_csv(BUDGET_FILE)

budget["start_date"] = pd.to_datetime(
    budget["start_date"],
    errors="coerce"
)

budget["end_date"] = pd.to_datetime(
    budget["end_date"],
    errors="coerce"
)

budget["budget_version_date"] = pd.to_datetime(
    budget["budget_version_date"],
    errors="coerce"
)


# ============================================================
# 8. MERGE BUDGET WITH PERFORMANCE
# ============================================================

print("Joining campaign budget...")

budget_columns = [
    "campaign_id",
    "owner",
    "budget_type",
    "daily_budget",
    "total_budget",
    "approved_budget",
    "target_conversions",
    "target_CPA",
    "target_revenue",
    "target_ROAS",
    "start_date",
    "end_date"
]

budget_subset = budget[budget_columns].copy()

paid_media = paid_media.merge(
    budget_subset,
    on="campaign_id",
    how="left"
)


# ============================================================
# 9. CALCULATE BUDGET UTILIZATION
# ============================================================

paid_media["budget_utilization"] = safe_divide(
    paid_media["spend"],
    paid_media["approved_budget"]
) * 100


# ============================================================
# 10. CALCULATE EXPECTED SPEND
# ============================================================

paid_media["days_elapsed"] = (
    paid_media["date"] -
    paid_media["start_date"]
).dt.days + 1

paid_media["days_elapsed"] = paid_media["days_elapsed"].clip(
    lower=1
)

paid_media["expected_spend_to_date"] = (
    paid_media["daily_budget"] *
    paid_media["days_elapsed"]
)

# Do not allow expected spend to exceed approved budget
paid_media["expected_spend_to_date"] = np.minimum(
    paid_media["expected_spend_to_date"],
    paid_media["approved_budget"]
)


# ============================================================
# 11. PACING VARIANCE
# ============================================================

paid_media["pacing_variance"] = (
    paid_media["spend"] -
    paid_media["expected_spend_to_date"]
)


# ============================================================
# 12. FORECAST SPEND
# ============================================================

period_days = (
    paid_media["end_date"] -
    paid_media["start_date"]
).dt.days + 1

paid_media["forecast_spend"] = safe_divide(
    paid_media["spend"],
    paid_media["days_elapsed"]
) * period_days


# ============================================================
# 13. BUDGET STATUS
# ============================================================

def determine_budget_status(row):

    if pd.isna(row["approved_budget"]):
        return "Insufficient Data"

    if row["spend"] == 0:
        return "Underspending"

    if row["pacing_variance"] > 0:
        return "Overspending"

    return "On Track"


paid_media["budget_status"] = paid_media.apply(
    determine_budget_status,
    axis=1
)


# ============================================================
# 14. ROI STATUS
# ============================================================

def determine_roi_status(row):

    if row["spend"] == 0:
        return "Insufficient Data"

    if row["roi"] > 0:
        return "Positive ROI"

    if row["roi"] == 0:
        return "Break-even"

    return "Negative ROI"


paid_media["roi_status"] = paid_media.apply(
    determine_roi_status,
    axis=1
)


# ============================================================
# 15. ROUND KPI VALUES
# ============================================================

round_columns = [
    "spend",
    "conversion_value",
    "ctr",
    "cpc",
    "cpm",
    "conversion_rate",
    "cpa",
    "cpl",
    "roas",
    "roi",
    "budget_utilization",
    "expected_spend_to_date",
    "pacing_variance",
    "forecast_spend"
]

for column in round_columns:
    paid_media[column] = paid_media[column].round(2)


# ============================================================
# 16. SORT DATA
# ============================================================

paid_media = paid_media.sort_values(
    [
        "date",
        "platform",
        "campaign_id"
    ]
).reset_index(drop=True)


# ============================================================
# 17. SAVE UNIFIED DATASET
# ============================================================

output_file = (
    PROCESSED_DIR /
    "unified_paid_media_daily.csv"
)

paid_media.to_csv(
    output_file,
    index=False
)


# ============================================================
# 18. CREATE CAMPAIGN SUMMARY
# ============================================================

print("\nCreating campaign-level summary...")

campaign_summary = (
    paid_media
    .groupby(
        [
            "campaign_id",
            "platform",
            "account_id",
            "campaign_name",
            "objective"
        ],
        as_index=False
    )
    .agg(
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        reach=("reach", "max"),
        clicks=("clicks", "sum"),
        leads=("leads", "sum"),
        conversions=("conversions", "sum"),
        revenue=("conversion_value", "sum"),
        approved_budget=("approved_budget", "first"),
        target_conversions=("target_conversions", "first"),
        target_CPA=("target_CPA", "first"),
        target_revenue=("target_revenue", "first"),
        target_ROAS=("target_ROAS", "first")
    )
)


# ============================================================
# 19. CAMPAIGN-LEVEL KPIs
# ============================================================

campaign_summary["ctr"] = (
    safe_divide(
        campaign_summary["clicks"],
        campaign_summary["impressions"]
    ) * 100
)

campaign_summary["cpc"] = safe_divide(
    campaign_summary["spend"],
    campaign_summary["clicks"]
)

campaign_summary["cpm"] = (
    safe_divide(
        campaign_summary["spend"],
        campaign_summary["impressions"]
    ) * 1000
)

campaign_summary["conversion_rate"] = (
    safe_divide(
        campaign_summary["conversions"],
        campaign_summary["clicks"]
    ) * 100
)

campaign_summary["cpa"] = safe_divide(
    campaign_summary["spend"],
    campaign_summary["conversions"]
)

campaign_summary["cpl"] = safe_divide(
    campaign_summary["spend"],
    campaign_summary["leads"]
)

campaign_summary["roas"] = safe_divide(
    campaign_summary["revenue"],
    campaign_summary["spend"]
)

campaign_summary["roi"] = (
    safe_divide(
        campaign_summary["revenue"] -
        campaign_summary["spend"],
        campaign_summary["spend"]
    ) * 100
)

campaign_summary["budget_utilization"] = (
    safe_divide(
        campaign_summary["spend"],
        campaign_summary["approved_budget"]
    ) * 100
)


# ============================================================
# 20. SAVE CAMPAIGN SUMMARY
# ============================================================

campaign_output = (
    PROCESSED_DIR /
    "campaign_performance_summary.csv"
)

campaign_summary.to_csv(
    campaign_output,
    index=False
)


# ============================================================
# 21. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("TRANSFORMATION COMPLETE")
print("=" * 70)

print(f"Unified dataset : {output_file}")
print(f"Campaign summary: {campaign_output}")

print(f"\nUnified rows    : {len(paid_media):,}")
print(f"Campaigns       : {paid_media['campaign_id'].nunique():,}")
print(f"Platforms       : {paid_media['platform'].nunique():,}")

print("\nPlatforms:")
print(
    paid_media["platform"]
    .value_counts()
    .to_string()
)

print("\nTotal Spend:")
print(
    f"${paid_media['spend'].sum():,.2f}"
)

print("\nTotal Conversions:")
print(
    f"{paid_media['conversions'].sum():,.0f}"
)

print("\nTotal Revenue:")
print(
    f"${paid_media['conversion_value'].sum():,.2f}"
)

print("\n" + "=" * 70)
print("SUCCESS ✅")
print("=" * 70)