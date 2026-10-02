from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


# ============================================================
# DATASET CONFIGURATION
# ============================================================

DATASETS = {
    "Campaign Budget": {
        "path": DATA_DIR / "synthetic" / "campaign_budget.csv",
        "required_columns": [
            "campaign_id",
            "platform",
            "account_id",
            "campaign_name",
            "objective",
            "start_date",
            "end_date",
            "currency",
            "total_budget",
            "approved_budget",
            "target_conversions",
            "target_CPA",
            "target_revenue",
            "target_ROAS",
        ],
    },

    "Google Ads": {
        "path": DATA_DIR / "raw" / "google_ads" / "daily_campaign_performance.csv",
        "required_columns": [
            "date",
            "campaign_id",
            "platform",
            "account_id",
            "campaign_name",
            "objective",
            "spend",
            "impressions",
            "clicks",
            "leads",
            "conversions",
            "conversion_value",
            "currency",
        ],
    },

    "Meta Ads": {
        "path": DATA_DIR / "raw" / "meta" / "daily_campaign_performance.csv",
        "required_columns": [
            "date",
            "campaign_id",
            "platform",
            "account_id",
            "campaign_name",
            "objective",
            "spend",
            "impressions",
            "clicks",
            "leads",
            "conversions",
            "conversion_value",
            "currency",
        ],
    },

    "LinkedIn Ads": {
        "path": DATA_DIR / "raw" / "linkedin" / "daily_campaign_performance.csv",
        "required_columns": [
            "date",
            "campaign_id",
            "platform",
            "account_id",
            "campaign_name",
            "objective",
            "spend",
            "impressions",
            "clicks",
            "leads",
            "conversions",
            "conversion_value",
            "currency",
        ],
    },

    "GA4": {
        "path": DATA_DIR / "raw" / "ga4" / "ga4_daily_channel.csv",
        "required_columns": [
            "date",
            "channel",
            "source",
            "medium",
            "users",
            "new_users",
            "sessions",
            "engaged_sessions",
            "engagement_rate",
            "conversions",
            "revenue",
        ],
    },

    "Google Search Console": {
        "path": DATA_DIR / "raw" / "gsc" / "gsc_daily_queries.csv",
        "required_columns": [
            "date",
            "query",
            "page",
            "country",
            "device",
            "search_type",
            "clicks",
            "impressions",
            "ctr",
            "average_position",
        ],
    },
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def check_file_exists(name, config):
    path = config["path"]

    if path.exists():
        print(f"✅ {name}: File exists")
        return True

    print(f"❌ {name}: File NOT FOUND")
    print(f"   Expected: {path}")
    return False


def check_columns(name, df, required_columns):
    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if not missing:
        print(f"✅ {name}: Required columns present")
        return True

    print(f"❌ {name}: Missing columns")
    for column in missing:
        print(f"   - {column}")

    return False


def check_duplicates(name, df):
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        print(f"✅ {name}: No duplicate rows")
        return True

    print(f"⚠️ {name}: {duplicates} duplicate rows found")
    return False


def check_missing_values(name, df):
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print(f"✅ {name}: No missing values")
        return True

    print(f"⚠️ {name}: Missing values found")

    for column, count in missing.items():
        print(f"   - {column}: {count}")

    return False


def check_negative_values(name, df):
    numeric_columns = [
        "spend",
        "impressions",
        "clicks",
        "leads",
        "conversions",
        "conversion_value",
        "users",
        "new_users",
        "sessions",
        "engaged_sessions",
        "revenue",
        "target_conversions",
        "total_budget",
        "approved_budget",
    ]

    problems = []

    for column in numeric_columns:
        if column in df.columns:
            negative_count = (df[column] < 0).sum()

            if negative_count > 0:
                problems.append((column, negative_count))

    if not problems:
        print(f"✅ {name}: No negative values in key metrics")
        return True

    print(f"❌ {name}: Negative values found")

    for column, count in problems:
        print(f"   - {column}: {count}")

    return False


def check_dates(name, df):
    if "date" not in df.columns:
        return True

    dates = pd.to_datetime(df["date"], errors="coerce")

    invalid = dates.isna().sum()

    if invalid == 0:
        print(f"✅ {name}: Valid dates")
        print(f"   Range: {dates.min().date()} → {dates.max().date()}")
        return True

    print(f"❌ {name}: {invalid} invalid dates")
    return False


def check_campaign_ids(name, df):
    if "campaign_id" not in df.columns:
        return True

    missing_ids = df["campaign_id"].isna().sum()

    if missing_ids == 0:
        print(f"✅ {name}: Campaign IDs present")
        return True

    print(f"❌ {name}: {missing_ids} missing campaign IDs")
    return False


# ============================================================
# MAIN VALIDATION
# ============================================================

def validate_dataset(name, config):

    print_header(name)

    if not check_file_exists(name, config):
        return False

    df = pd.read_csv(config["path"])

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    results = []

    results.append(
        check_columns(
            name,
            df,
            config["required_columns"]
        )
    )

    results.append(
        check_duplicates(name, df)
    )

    results.append(
        check_missing_values(name, df)
    )

    results.append(
        check_negative_values(name, df)
    )

    results.append(
        check_dates(name, df)
    )

    results.append(
        check_campaign_ids(name, df)
    )

    return all(results)


def main():

    print_header("MARKETING PERFORMANCE DASHBOARD")
    print("DATASET VALIDATION")
    print(f"Project directory: {BASE_DIR}")

    results = {}

    for name, config in DATASETS.items():
        results[name] = validate_dataset(name, config)

    print_header("VALIDATION SUMMARY")

    passed = 0
    failed = 0

    for name, result in results.items():

        if result:
            print(f"✅ PASS  - {name}")
            passed += 1

        else:
            print(f"❌ FAIL  - {name}")
            failed += 1

    print("\n" + "-" * 70)

    print(f"Datasets Passed : {passed}")
    print(f"Datasets Failed : {failed}")

    if failed == 0:
        print("\n🎉 ALL DATASETS PASSED VALIDATION!")
    else:
        print("\n⚠️ SOME DATASETS REQUIRE ATTENTION")


if __name__ == "__main__":
    main()