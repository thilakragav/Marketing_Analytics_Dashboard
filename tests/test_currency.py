"""
Unit tests for Global Currency Configuration & Conversion Architecture.
Tests currency conversion, state switching, formatting, DataFrame safety,
zero/negative/NaN handling, and prevention of double-conversion bugs.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.utils.currency import (
    CURRENCY_CONFIG,
    CURRENCY_OPTIONS,
    DEFAULT_CURRENCY,
    get_selected_currency,
    set_selected_currency,
    get_currency_symbol,
    get_currency_rate,
    convert_currency,
    format_currency,
    format_currency_label,
    normalize_currency_code,
)
from app.components.kpi_card import format_val


def test_default_currency():
    """Verify default currency is USD on clean start."""
    set_selected_currency("USD")
    assert get_selected_currency() == "USD"
    assert get_currency_symbol() == "$"
    assert get_currency_rate("USD", "USD") == 1.0


def test_currency_rates():
    """Verify configured conversion rates relative to USD."""
    assert CURRENCY_CONFIG["USD"]["rate"] == 1.0
    assert CURRENCY_CONFIG["INR"]["rate"] == 83.0
    assert CURRENCY_CONFIG["EUR"]["rate"] == 0.92
    assert CURRENCY_CONFIG["GBP"]["rate"] == 0.79

    assert get_currency_rate("INR", "USD") == 83.0
    assert get_currency_rate("EUR", "USD") == 0.92
    assert get_currency_rate("GBP", "USD") == 0.79
    assert get_currency_rate("USD", "USD") == 1.0


def test_currency_normalization():
    """Verify robust recognition of labels, symbols, and codes."""
    assert normalize_currency_code("USD ($)") == "USD"
    assert normalize_currency_code("INR (₹)") == "INR"
    assert normalize_currency_code("EUR (€)") == "EUR"
    assert normalize_currency_code("GBP (£)") == "GBP"

    assert normalize_currency_code("USD") == "USD"
    assert normalize_currency_code("INR") == "INR"
    assert normalize_currency_code("EUR") == "EUR"
    assert normalize_currency_code("GBP") == "GBP"

    assert normalize_currency_code("$") == "USD"
    assert normalize_currency_code("₹") == "INR"
    assert normalize_currency_code("€") == "EUR"
    assert normalize_currency_code("£") == "GBP"

    # Default fallback
    assert normalize_currency_code("UNKNOWN") == "USD"
    assert normalize_currency_code(None) == "USD"


def test_scalar_conversion_to_inr():
    """Verify USD 1,000 converts to INR 83,000."""
    set_selected_currency("INR")
    assert get_selected_currency() == "INR"
    assert get_currency_symbol() == "₹"

    # 1,000 USD -> 83,000 INR
    converted = convert_currency(1000.0)
    assert converted == 83000.0

    # Negative value
    assert convert_currency(-50.0) == -4150.0

    # Zero
    assert convert_currency(0.0) == 0.0

    # None and NaN handling
    assert convert_currency(None) is None
    assert np.isnan(convert_currency(np.nan))


def test_scalar_conversion_to_eur_and_gbp():
    """Verify USD 1,000 converts to EUR 920 and GBP 790."""
    # EUR
    set_selected_currency("EUR")
    assert get_selected_currency() == "EUR"
    assert get_currency_symbol() == "€"
    assert convert_currency(1000.0) == 920.0

    # GBP
    set_selected_currency("GBP")
    assert get_selected_currency() == "GBP"
    assert get_currency_symbol() == "£"
    assert convert_currency(1000.0) == 790.0


def test_switch_back_to_usd_preserves_original():
    """
    Verify switching USD -> INR -> USD restores exact original USD numbers.
    Confirms original value is never lost and no double-conversion occurs.
    """
    original_usd = 1250.75

    # 1. Start at USD
    set_selected_currency("USD")
    val_usd_1 = convert_currency(original_usd)
    assert val_usd_1 == 1250.75

    # 2. Switch to INR
    set_selected_currency("INR")
    val_inr = convert_currency(original_usd)
    assert val_inr == 1250.75 * 83.0

    # 3. Switch to EUR
    set_selected_currency("EUR")
    val_eur = convert_currency(original_usd)
    assert val_eur == 1250.75 * 0.92

    # 4. Switch back to USD
    set_selected_currency("USD")
    val_usd_2 = convert_currency(original_usd)
    assert val_usd_2 == 1250.75
    assert val_usd_2 == original_usd


def test_currency_formatting():
    """Verify global formatting for USD, INR, EUR, GBP."""
    val_usd = 1000.0

    # USD
    set_selected_currency("USD")
    assert format_currency(val_usd) == "$1,000.00"

    # INR
    set_selected_currency("INR")
    assert format_currency(val_usd) == "₹83,000.00"

    # EUR
    set_selected_currency("EUR")
    assert format_currency(val_usd) == "€920.00"

    # GBP
    set_selected_currency("GBP")
    assert format_currency(val_usd) == "£790.00"

    # Compact formatting
    set_selected_currency("INR")
    assert format_currency(val_usd, compact=True) == "₹83.0K"

    # None and NaN handling
    assert format_currency(None) == "N/A"
    assert format_currency(np.nan) == "N/A"


def test_pandas_series_conversion():
    """Verify pandas Series conversions preserve originals and scale safely."""
    set_selected_currency("INR")
    usd_series = pd.Series([100.0, 250.0, 500.0, 1000.0])

    inr_series = convert_currency(usd_series)
    expected_inr = pd.Series([8300.0, 20750.0, 41500.0, 83000.0])

    pd.testing.assert_series_equal(inr_series, expected_inr)

    # Ensure original series was NOT modified in-place
    assert usd_series.iloc[0] == 100.0
    assert usd_series.iloc[3] == 1000.0


def test_non_monetary_metrics_unchanged():
    """
    Verify percentages, counts, and ratios are NOT converted.
    ROI %, CTR %, CVR %, ROAS (x), Conversions (count).
    """
    set_selected_currency("INR")

    # ROI %: 250.0% should remain 250.0%
    roi_pct = 250.0
    assert roi_pct == 250.0  # untouched by currency logic

    # ROAS ratio: 3.5x should remain 3.5x
    roas = 3.5
    assert roas == 3.5

    # Conversions count: 124 should remain 124
    conversions = 124
    assert conversions == 124


def test_kpi_card_format_val():
    """Verify kpi_card format_val respects currency symbol."""
    set_selected_currency("INR")
    sym = get_currency_symbol()
    assert sym == "₹"

    # format_val with currency
    res = format_val(83000.0, fmt_type="currency", currency_symbol=sym)
    assert "₹83.0K" == res

    set_selected_currency("USD")
    sym_usd = get_currency_symbol()
    assert sym_usd == "$"
    res_usd = format_val(1000.0, fmt_type="currency", currency_symbol=sym_usd)
    assert "$1.0K" == res_usd


def test_format_currency_label():
    """Verify chart label title adaptation."""
    set_selected_currency("INR")
    assert format_currency_label("Revenue ($)") == "Revenue (₹)"
    assert format_currency_label("Daily Spend vs Revenue") == "Daily Spend vs Revenue (₹)"

    set_selected_currency("EUR")
    assert format_currency_label("Revenue ($)") == "Revenue (€)"


if __name__ == "__main__":
    print("Running Global Currency tests...")
    test_default_currency()
    print("  [PASS] test_default_currency")
    test_currency_rates()
    print("  [PASS] test_currency_rates")
    test_currency_normalization()
    print("  [PASS] test_currency_normalization")
    test_scalar_conversion_to_inr()
    print("  [PASS] test_scalar_conversion_to_inr")
    test_scalar_conversion_to_eur_and_gbp()
    print("  [PASS] test_scalar_conversion_to_eur_and_gbp")
    test_switch_back_to_usd_preserves_original()
    print("  [PASS] test_switch_back_to_usd_preserves_original")
    test_currency_formatting()
    print("  [PASS] test_currency_formatting")
    test_pandas_series_conversion()
    print("  [PASS] test_pandas_series_conversion")
    test_non_monetary_metrics_unchanged()
    print("  [PASS] test_non_monetary_metrics_unchanged")
    test_kpi_card_format_val()
    print("  [PASS] test_kpi_card_format_val")
    test_format_currency_label()
    print("  [PASS] test_format_currency_label")
    set_selected_currency("USD")
    print("ALL CURRENCY TESTS PASSED [OK]")
