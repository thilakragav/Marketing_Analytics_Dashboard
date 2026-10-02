from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
from app.components.charts import apply_geo_map_theme, apply_chart_theme
from app.utils.currency import get_selected_currency, get_currency_symbol, convert_currency, format_currency

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "data" / "processed" / "global_geographic_sales.csv"


def load_geo_sales_data(engine=None) -> pd.DataFrame:
    """
    Loads global geographic sales performance data from PostgreSQL table
    'global_geographic_sales' or falls back to 'data/processed/global_geographic_sales.csv'.
    Underlying raw monetary values remain strictly in USD.
    """
    if engine is not None:
        try:
            with engine.connect() as conn:
                df = pd.read_sql("SELECT * FROM global_geographic_sales ORDER BY sales_revenue_usd DESC", conn)
                if not df.empty:
                    return df
        except Exception:
            pass

    if CSV_FILE.exists():
        return pd.read_csv(CSV_FILE)

    # Minimal fallback dataframe if file is not found
    return pd.DataFrame([
        {"country_code": "USA", "country_name": "United States", "region": "North America", "flag": "🇺🇸", "latitude": 37.09, "longitude": -95.71, "sales_revenue_usd": 21660000.0, "orders_count": 136000, "ad_spend_usd": 1050000.0, "aov_usd": 159.2, "roas": 20.6, "market_share_pct": 42.5, "growth_rate_pct": 14.8},
        {"country_code": "GBR", "country_name": "United Kingdom", "region": "Europe", "flag": "🇬🇧", "latitude": 55.37, "longitude": -3.43, "sales_revenue_usd": 6220000.0, "orders_count": 39000, "ad_spend_usd": 300000.0, "aov_usd": 158.5, "roas": 20.7, "market_share_pct": 12.2, "growth_rate_pct": 11.2},
        {"country_code": "IND", "country_name": "India", "region": "Asia-Pacific", "flag": "🇮🇳", "latitude": 20.59, "longitude": 78.96, "sales_revenue_usd": 5500000.0, "orders_count": 48000, "ad_spend_usd": 2650000.0, "aov_usd": 114.5, "roas": 20.8, "market_share_pct": 10.8, "growth_rate_pct": 28.4},
    ])


def prepare_display_geo_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a presentation-layer copy of the geographic sales data with
    monetary values converted into the currently active global currency.
    The original USD values in df are never modified.
    """
    df_disp = df.copy()
    sym = get_currency_symbol()

    # Dynamic presentation conversion
    df_disp["sales_revenue_converted"] = convert_currency(df_disp["sales_revenue_usd"])
    df_disp["ad_spend_converted"] = convert_currency(df_disp["ad_spend_usd"])
    df_disp["aov_converted"] = convert_currency(df_disp["aov_usd"])

    # Human-formatted text columns for hover and display tables
    df_disp["sales_formatted"] = df_disp["sales_revenue_converted"].apply(lambda v: f"{sym}{v:,.2f}")
    df_disp["spend_formatted"] = df_disp["ad_spend_converted"].apply(lambda v: f"{sym}{v:,.2f}")
    df_disp["aov_formatted"] = df_disp["aov_converted"].apply(lambda v: f"{sym}{v:,.2f}")
    df_disp["orders_formatted"] = df_disp["orders_count"].apply(lambda v: f"{v:,}")

    return df_disp


def build_world_choropleth_map(
    df: pd.DataFrame,
    metric: str = "sales_revenue",
    projection: str = "natural earth",
    height: int = 540
) -> go.Figure:
    """
    Generates an enterprise-grade dark cyber Choropleth map.
    Supported metrics:
    - 'sales_revenue': Total Sales / Revenue (converted to active currency)
    - 'orders_count': Total Orders / Conversions (count)
    - 'roas': Return on Ad Spend (multiplier)
    - 'aov': Average Order Value (converted to active currency)
    - 'growth_rate_pct': YoY Growth Rate (%)
    """
    df_disp = prepare_display_geo_data(df)
    sym = get_currency_symbol()
    curr_code = get_selected_currency()

    if metric == "sales_revenue":
        color_col = "sales_revenue_converted"
        color_label = f"Sales ({sym})"
        colorscale = [
            [0.0, "#0A192F"],
            [0.15, "#0E3A5D"],
            [0.35, "#0284C7"],
            [0.65, "#38BDF8"],
            [0.85, "#4ADE80"],
            [1.0, "#FACC15"]
        ]
        title_text = f"Global Sales Revenue Distribution ({curr_code} {sym})"
    elif metric == "orders_count":
        color_col = "orders_count"
        color_label = "Orders"
        colorscale = [
            [0.0, "#0F172A"],
            [0.2, "#312E81"],
            [0.5, "#6366F1"],
            [0.8, "#A855F7"],
            [1.0, "#EC4899"]
        ]
        title_text = "Global Orders & Customer Transactions Volume"
    elif metric == "roas":
        color_col = "roas"
        color_label = "ROAS (x)"
        colorscale = [
            [0.0, "#064E3B"],
            [0.3, "#047857"],
            [0.6, "#10B981"],
            [0.85, "#34D399"],
            [1.0, "#6EE7B7"]
        ]
        title_text = "Global Marketing Efficiency & ROAS by Country"
    elif metric == "aov":
        color_col = "aov_converted"
        color_label = f"AOV ({sym})"
        colorscale = [
            [0.0, "#1E1B4B"],
            [0.3, "#4338CA"],
            [0.6, "#818CF8"],
            [0.85, "#C084FC"],
            [1.0, "#F472B6"]
        ]
        title_text = f"Global Average Order Value (AOV in {curr_code} {sym})"
    else:  # growth_rate_pct
        color_col = "growth_rate_pct"
        color_label = "YoY Growth %"
        colorscale = [
            [0.0, "#1E293B"],
            [0.3, "#0284C7"],
            [0.7, "#10B981"],
            [1.0, "#F59E0B"]
        ]
        title_text = "Global Annual Sales Growth Rate (% YoY)"

    fig = px.choropleth(
        df_disp,
        locations="country_code",
        color=color_col,
        hover_name="country_name",
        hover_data={
            "country_code": False,
            color_col: False,
            "region": True,
            "sales_formatted": True,
            "orders_formatted": True,
            "aov_formatted": True,
            "roas": ":.2f",
            "market_share_pct": ":.2f",
            "growth_rate_pct": ":.1f",
        },
        labels={
            "region": "Region",
            "sales_formatted": f"Sales ({sym})",
            "orders_formatted": "Orders",
            "aov_formatted": f"AOV ({sym})",
            "roas": "ROAS (x)",
            "market_share_pct": "Market Share %",
            "growth_rate_pct": "Growth %",
            color_col: color_label
        },
        color_continuous_scale=colorscale,
        projection=projection
    )

    # Custom crisp hovercard template
    custom_hover = (
        "<b>%{hovertext}</b> (%{customdata[0]})<br>"
        "<span style='color: #38BDF8;'>━━━━━━━━━━━━━━━━━━━━━━</span><br>"
        f"<b>Total Sales:</b> %{{customdata[1]}}<br>"
        "<b>Orders Count:</b> %{customdata[2]}<br>"
        f"<b>Average Order Value:</b> %{{customdata[3]}}<br>"
        "<b>ROAS Efficiency:</b> %{customdata[4]}x<br>"
        "<b>Global Market Share:</b> %{customdata[5]}%<br>"
        "<b>Annual Growth:</b> +%{customdata[6]}%<br>"
        "<extra></extra>"
    )
    fig.update_traces(
        hovertemplate=custom_hover,
        marker_line_color="rgba(56, 189, 248, 0.4)",
        marker_line_width=0.6
    )

    apply_geo_map_theme(fig, title=title_text, height=height)
    return fig


def build_world_bubble_map(
    df: pd.DataFrame,
    metric: str = "sales_revenue",
    projection: str = "natural earth",
    height: int = 540
) -> go.Figure:
    """
    Generates an illuminated scatter geo bubble map where glowing points are sized
    proportionately to sales volume or orders at the country coordinates.
    """
    df_disp = prepare_display_geo_data(df)
    sym = get_currency_symbol()
    curr_code = get_selected_currency()

    size_col = "sales_revenue_converted" if metric == "sales_revenue" else "orders_count"
    title_text = f"Global Sales Activity Spheres ({curr_code} {sym})" if metric == "sales_revenue" else "Global Orders Activity Spheres"

    fig = go.Figure()

    # Base scattergeo bubbles
    fig.add_trace(
        go.Scattergeo(
            lon=df_disp["longitude"],
            lat=df_disp["latitude"],
            text=df_disp["country_name"],
            customdata=df_disp[["region", "sales_formatted", "orders_formatted", "aov_formatted", "roas", "market_share_pct", "growth_rate_pct"]].values,
            hovertemplate=(
                "<b>%{text}</b> (%{customdata[0]})<br>"
                "<span style='color: #38BDF8;'>━━━━━━━━━━━━━━━━━━━━━━</span><br>"
                f"<b>Total Sales:</b> %{{customdata[1]}}<br>"
                "<b>Orders:</b> %{customdata[2]}<br>"
                f"<b>AOV:</b> %{{customdata[3]}}<br>"
                "<b>ROAS:</b> %{customdata[4]}x<br>"
                "<b>Market Share:</b> %{customdata[5]}%<br>"
                "<extra></extra>"
            ),
            mode="markers+text",
            textposition="top center",
            textfont=dict(color="#F8FAFC", size=9, family="'Plus Jakarta Sans', sans-serif"),
            marker=dict(
                size=np.sqrt(df_disp[size_col]) / (np.sqrt(df_disp[size_col].max()) / 38) + 8,
                color=df_disp["sales_revenue_converted"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(
                    title=dict(text=f"Sales ({sym})", font=dict(color="#94A3B8", size=11)),
                    tickfont=dict(color="#94A3B8", size=10),
                    thickness=14,
                    len=0.75,
                    x=0.98,
                    bgcolor="rgba(10, 16, 28, 0.6)",
                    outlinecolor="rgba(56, 189, 248, 0.2)",
                    outlinewidth=1
                ),
                line=dict(width=1.5, color="#38BDF8"),
                opacity=0.88
            )
        )
    )

    fig.update_geos(projection_type=projection)
    apply_geo_map_theme(fig, title=title_text, height=height)
    return fig


def get_regional_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes regional totals with currency conversions.
    """
    df_disp = prepare_display_geo_data(df)
    grouped = df_disp.groupby("region").agg(
        total_sales=("sales_revenue_converted", "sum"),
        total_spend=("ad_spend_converted", "sum"),
        total_orders=("orders_count", "sum"),
        country_count=("country_code", "count"),
        avg_growth=("growth_rate_pct", "mean")
    ).reset_index()

    grouped["roas"] = (grouped["total_sales"] / grouped["total_spend"]).round(2)
    grouped["aov"] = (grouped["total_sales"] / grouped["total_orders"]).round(2)
    total_sales_all = grouped["total_sales"].sum()
    grouped["sales_share_pct"] = ((grouped["total_sales"] / total_sales_all) * 100).round(2)
    grouped = grouped.sort_values(by="total_sales", ascending=False).reset_index(drop=True)

    return grouped


def build_regional_share_donut(df_regional: pd.DataFrame) -> go.Figure:
    """Donut chart for continental / regional sales share."""
    sym = get_currency_symbol()
    fig = px.pie(
        df_regional,
        values="total_sales",
        names="region",
        hole=0.48,
        color_discrete_sequence=["#38BDF8", "#FF4D5A", "#10B981", "#F59E0B", "#A855F7"]
    )
    apply_chart_theme(fig, title=f"Regional Sales Distribution ({sym})", height=320)
    return fig


def build_top_markets_bar_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart showing the highest sales countries."""
    df_disp = prepare_display_geo_data(df).head(top_n).iloc[::-1]
    sym = get_currency_symbol()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=df_disp["flag"] + " " + df_disp["country_name"],
            x=df_disp["sales_revenue_converted"],
            orientation="h",
            marker=dict(
                color=df_disp["sales_revenue_converted"],
                colorscale=[[0, "#0284C7"], [1, "#38BDF8"]],
                line=dict(color="#38BDF8", width=1)
            ),
            customdata=df_disp[["sales_formatted", "market_share_pct", "roas"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                f"<b>Sales:</b> %{{customdata[0]}}<br>"
                "<b>Market Share:</b> %{customdata[1]}%<br>"
                "<b>ROAS:</b> %{customdata[2]}x<extra></extra>"
            )
        )
    )

    apply_chart_theme(fig, title=f"Top {top_n} Global Markets by Sales Volume ({sym})", height=340)
    fig.update_layout(xaxis_title=f"Sales Volume ({sym})", yaxis_title="")
    return fig
