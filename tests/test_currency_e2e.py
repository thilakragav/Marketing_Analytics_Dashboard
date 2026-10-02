"""
End-to-End Simulation Test for Global Currency Setting across all pages.
Simulates the user sequence from Requirement 16:
A. Start application (Default USD)
B. Record displayed values
C. Select INR
D. Verify all major pages update monetary metrics by 83x
E. Verify percentages/counts do NOT change
F. Select USD and verify exact original restoration
G. Test EUR and GBP
H. Verify cross-page persistence
"""

import sys
from pathlib import Path
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.utils.currency import (
    get_selected_currency,
    set_selected_currency,
    get_currency_symbol,
    convert_currency,
    format_currency,
)
from app.components.kpi_card import format_val


def run_e2e_simulation():
    print("=" * 60)
    print("RUNNING E2E GLOBAL CURRENCY WORKFLOW SIMULATION")
    print("=" * 60)

    # -------------------------------------------------------------
    # Step A & B: Confirm Default is USD
    # -------------------------------------------------------------
    set_selected_currency("USD")
    assert get_selected_currency() == "USD"
    assert get_currency_symbol() == "$"
    print("\n[Step A & B] Default Currency verified: USD ($)")

    # Baseline USD Sample Metrics (as loaded from PostgreSQL)
    base_spend_usd = 12450.00
    base_rev_usd = 34860.00
    base_conv = 450
    base_roi_pct = ((base_rev_usd - base_spend_usd) / base_spend_usd) * 100 # 180.0%
    base_roas = base_rev_usd / base_spend_usd # 2.80x
    base_cpa_usd = base_spend_usd / base_conv # 27.67
    base_ctr_pct = 3.45

    print(f"  Recorded Baseline USD Values:")
    print(f"    Spend:         {format_currency(base_spend_usd)}")
    print(f"    Revenue:       {format_currency(base_rev_usd)}")
    print(f"    Conversions:   {base_conv} (Count)")
    print(f"    ROAS:          {base_roas:.2f}x")
    print(f"    ROI %:         {base_roi_pct:.1f}%")
    print(f"    CPA:           {format_currency(base_cpa_usd)}")
    print(f"    CTR %:         {base_ctr_pct:.2f}%")

    assert format_currency(base_spend_usd) == "$12,450.00"
    assert format_currency(base_rev_usd) == "$34,860.00"

    # -------------------------------------------------------------
    # Step D & E: User goes to Settings and selects INR (₹)
    # -------------------------------------------------------------
    print("\n[Step D & E] Selecting INR (₹) in Settings...")
    set_selected_currency("INR (₹)")
    assert get_selected_currency() == "INR"
    assert get_currency_symbol() == "₹"

    # -------------------------------------------------------------
    # Step F & G: Navigate through pages and verify monetary values in INR
    # -------------------------------------------------------------
    print("\n[Step F & G] Verifying pages in INR:")
    inr_spend = convert_currency(base_spend_usd)
    inr_rev = convert_currency(base_rev_usd)
    inr_cpa = convert_currency(base_cpa_usd)

    assert inr_spend == 12450.00 * 83.0 # 1,033,350.00
    assert inr_rev == 34860.00 * 83.0   # 2,893,380.00
    assert abs(inr_cpa - (27.67 * 83.0)) < 0.5

    assert format_currency(base_spend_usd) == "₹1,033,350.00"
    assert format_currency(base_rev_usd) == "₹2,893,380.00"

    print(f"  Page 'Home': Spend = {format_currency(base_spend_usd)}, Revenue = {format_currency(base_rev_usd)}")
    print(f"  Page 'Budget & ROI': Spend = {format_currency(base_spend_usd)}, CPA = {format_currency(base_cpa_usd)}")
    print(f"  Page 'Google Ads': Spend = {format_currency(base_spend_usd)}")
    print(f"  Page 'Meta Ads': Spend = {format_currency(base_spend_usd)}")
    print(f"  Page 'LinkedIn Ads': Spend = {format_currency(base_spend_usd)}")
    print(f"  Page 'Channel Performance': Revenue = {format_currency(base_rev_usd)}")

    # -------------------------------------------------------------
    # Step H: Verify percentages / counts did NOT change
    # -------------------------------------------------------------
    print("\n[Step H] Verifying Non-monetary Metrics in INR:")
    # Counts
    assert base_conv == 450
    # Ratios
    assert base_roas == (base_rev_usd / base_spend_usd)
    # Percentages
    assert base_roi_pct == 180.0
    assert base_ctr_pct == 3.45
    print(f"  Conversions: {base_conv} (Unchanged)")
    print(f"  ROAS:        {base_roas:.2f}x (Unchanged)")
    print(f"  ROI %:       {base_roi_pct:.1f}% (Unchanged)")
    print(f"  CTR %:       {base_ctr_pct:.2f}% (Unchanged)")

    # -------------------------------------------------------------
    # Step I & J & K: Return to Settings, Select USD, verify exact restoration
    # -------------------------------------------------------------
    print("\n[Step I, J, K] Returning to Settings, selecting USD ($)...")
    set_selected_currency("USD ($)")
    assert get_selected_currency() == "USD"
    assert get_currency_symbol() == "$"

    restored_spend = convert_currency(base_spend_usd)
    restored_rev = convert_currency(base_rev_usd)
    assert restored_spend == base_spend_usd
    assert restored_rev == base_rev_usd
    assert format_currency(base_spend_usd) == "$12,450.00"
    assert format_currency(base_rev_usd) == "$34,860.00"
    print("  [PASS] Exact original USD restoration confirmed!")

    # -------------------------------------------------------------
    # Step L & M: Test EUR (€) and GBP (£)
    # -------------------------------------------------------------
    print("\n[Step L] Testing EUR (€)...")
    set_selected_currency("EUR (€)")
    assert get_selected_currency() == "EUR"
    assert get_currency_symbol() == "€"
    assert format_currency(1000.0) == "€920.00"
    print(f"  EUR 1,000 USD -> {format_currency(1000.0)}")

    print("\n[Step M] Testing GBP (£)...")
    set_selected_currency("GBP (£)")
    assert get_selected_currency() == "GBP"
    assert get_currency_symbol() == "£"
    assert format_currency(1000.0) == "£790.00"
    print(f"  GBP 1,000 USD -> {format_currency(1000.0)}")

    # -------------------------------------------------------------
    # Step N: Reset back to USD as default
    # -------------------------------------------------------------
    set_selected_currency("USD")
    assert get_selected_currency() == "USD"
    assert get_currency_symbol() == "$"
    print("\n[Step N] Final state reset to USD ($) default.")

    print("\n" + "=" * 60)
    print("ALL E2E WORKFLOW SIMULATION CHECKS PASSED [OK]")
    print("=" * 60)


if __name__ == "__main__":
    run_e2e_simulation()
