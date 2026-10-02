import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from app.services.geo_service import (
    load_geo_sales_data,
    prepare_display_geo_data,
    build_world_choropleth_map,
    build_world_bubble_map,
    get_regional_summary,
    build_top_markets_bar_chart,
    build_regional_share_donut
)
from app.utils.currency import set_selected_currency, get_selected_currency, get_currency_symbol, convert_currency


def test_geo_data_loading():
    df = load_geo_sales_data()
    assert not df.empty, "Geo dataset must not be empty"
    assert len(df) >= 30, f"Expected at least 30 countries, got {len(df)}"
    expected_cols = [
        "country_code", "country_name", "region", "flag",
        "sales_revenue_usd", "orders_count", "ad_spend_usd",
        "aov_usd", "roas", "market_share_pct", "growth_rate_pct"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing required column {col}"
    print("  [PASS] test_geo_data_loading")


def test_geo_currency_conversion():
    df = load_geo_sales_data()
    usa_row = df[df["country_code"] == "USA"].iloc[0]
    base_sales = usa_row["sales_revenue_usd"]

    # 1. USD Baseline
    set_selected_currency("USD")
    disp_usd = prepare_display_geo_data(df)
    usa_disp_usd = disp_usd[disp_usd["country_code"] == "USA"].iloc[0]
    assert usa_disp_usd["sales_revenue_converted"] == base_sales
    assert "$" in usa_disp_usd["sales_formatted"]

    # 2. INR Conversion
    set_selected_currency("INR")
    disp_inr = prepare_display_geo_data(df)
    usa_disp_inr = disp_inr[disp_inr["country_code"] == "USA"].iloc[0]
    assert round(usa_disp_inr["sales_revenue_converted"], 2) == round(base_sales * 83.0, 2)
    assert "₹" in usa_disp_inr["sales_formatted"]

    # 3. EUR Conversion
    set_selected_currency("EUR")
    disp_eur = prepare_display_geo_data(df)
    usa_disp_eur = disp_eur[disp_eur["country_code"] == "USA"].iloc[0]
    assert round(usa_disp_eur["sales_revenue_converted"], 2) == round(base_sales * 0.92, 2)
    assert "€" in usa_disp_eur["sales_formatted"]

    # 4. Return to USD
    set_selected_currency("USD")
    disp_restored = prepare_display_geo_data(df)
    usa_restored = disp_restored[disp_restored["country_code"] == "USA"].iloc[0]
    assert usa_restored["sales_revenue_converted"] == base_sales

    print("  [PASS] test_geo_currency_conversion")


def test_non_monetary_metrics_preserved():
    df = load_geo_sales_data()
    ind_row = df[df["country_code"] == "IND"].iloc[0]
    base_orders = ind_row["orders_count"]
    base_roas = ind_row["roas"]
    base_share = ind_row["market_share_pct"]

    set_selected_currency("INR")
    disp = prepare_display_geo_data(df)
    ind_disp = disp[disp["country_code"] == "IND"].iloc[0]

    assert ind_disp["orders_count"] == base_orders
    assert ind_disp["roas"] == base_roas
    assert ind_disp["market_share_pct"] == base_share

    set_selected_currency("USD")
    print("  [PASS] test_non_monetary_metrics_preserved")


def test_map_and_chart_builders():
    df = load_geo_sales_data()

    fig_choro = build_world_choropleth_map(df, metric="sales_revenue")
    assert fig_choro is not None
    assert len(fig_choro.data) >= 1

    fig_globe = build_world_choropleth_map(df, metric="sales_revenue", projection="orthographic")
    assert fig_globe is not None

    fig_bubble = build_world_bubble_map(df, metric="sales_revenue")
    assert fig_bubble is not None
    assert len(fig_bubble.data) >= 1

    fig_bar = build_top_markets_bar_chart(df, top_n=10)
    assert fig_bar is not None

    df_reg = get_regional_summary(df)
    assert len(df_reg) == 5, f"Expected 5 regions, got {len(df_reg)}"
    fig_donut = build_regional_share_donut(df_reg)
    assert fig_donut is not None

    print("  [PASS] test_map_and_chart_builders")


if __name__ == "__main__":
    print("Running Global Geographic Sales Map tests...")
    test_geo_data_loading()
    test_geo_currency_conversion()
    test_non_monetary_metrics_preserved()
    test_map_and_chart_builders()
    set_selected_currency("USD")
    print("ALL GEOGRAPHIC SALES TESTS PASSED [OK]")
