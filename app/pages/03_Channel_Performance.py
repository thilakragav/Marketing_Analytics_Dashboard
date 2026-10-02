import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from app.components.theme import apply_enterprise_theme
from app.components.sidebar import render_global_sidebar
from app.components.header import render_global_header
from app.components.kpi_card import render_kpi_card
from app.components.filter_bar import render_filter_bar
from app.components.ai_assistant import render_ai_assistant
from app.components.charts import apply_chart_theme

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Channel Performance",
    page_icon="📈",
    layout="wide"
)

apply_enterprise_theme()
render_global_sidebar()

# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_USER = "postgres"
DB_PASSWORD = st.secrets.get("DB_PASSWORD", "")
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "marketing_dashboard"

@st.cache_resource
def get_engine():
    if not DB_PASSWORD:
        return None
    encoded_password = quote_plus(DB_PASSWORD)
    database_url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{encoded_password}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(database_url)

engine = get_engine()

render_global_header(
    title="Cross-Channel Media Performance",
    description="Comparative multi-platform analysis across Google Ads, Meta Ads and LinkedIn Ads",
    icon="📈",
    engine=engine
)

if not engine:
    st.error("Database connection is not configured.")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=300)
def load_paid_media_channels():
    query = """
        SELECT
            date,
            platform,
            campaign_name,
            spend,
            impressions,
            clicks,
            leads,
            conversions,
            conversion_value
        FROM paid_media_daily
        ORDER BY date
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    df["date"] = pd.to_datetime(df["date"])
    return df

try:
    paid_df = load_paid_media_channels()
except Exception as e:
    st.error(f"Error loading channel data: {str(e)}")
    st.stop()

min_date = paid_df["date"].min().date()
max_date = paid_df["date"].max().date()
channels = sorted(paid_df["platform"].unique().tolist())

# ============================================================
# FILTER BAR
# ============================================================

filters = render_filter_bar(
    min_date=min_date,
    max_date=max_date,
    channel_options=channels,
    key_prefix="channel"
)

curr_df = paid_df[
    (paid_df["date"] >= filters["start_date"])
    & (paid_df["date"] <= filters["end_date"])
    & (paid_df["platform"].isin(filters["selected_channels"]))
]

prev_df = paid_df[
    (paid_df["date"] >= filters["comp_start"])
    & (paid_df["date"] <= filters["comp_end"])
    & (paid_df["platform"].isin(filters["selected_channels"]))
]

if curr_df.empty:
    st.warning("No data is available for the selected filters.")
    st.stop()

# Compute overall metrics
curr_spend = curr_df["spend"].sum()
prev_spend = prev_df["spend"].sum() if not prev_df.empty else 0.0

curr_rev = curr_df["conversion_value"].sum()
prev_rev = prev_df["conversion_value"].sum() if not prev_df.empty else 0.0

curr_conv = curr_df["conversions"].sum()
prev_conv = prev_df["conversions"].sum() if not prev_df.empty else 0.0

curr_cpa = (curr_spend / curr_conv) if curr_conv > 0 else 0.0
prev_cpa = (prev_spend / prev_conv) if prev_conv > 0 else 0.0

curr_roas = (curr_rev / curr_spend) if curr_spend > 0 else 0.0
prev_roas = (prev_rev / prev_spend) if prev_spend > 0 else 0.0

curr_roi = ((curr_rev - curr_spend) / curr_spend * 100) if curr_spend > 0 else 0.0
prev_roi = ((prev_rev - prev_spend) / prev_spend * 100) if prev_spend > 0 else 0.0

currency_sym = st.session_state.get("currency_symbol", "$")
comp_lbl = filters["comp_label"]
is_inc = filters["is_incomplete"]

# ============================================================
# KPI ROW: Spend, Revenue, Conversions, CPA, ROAS, ROI
# ============================================================

st.subheader("Cross-Channel Portfolio KPIs")

row1_cols = st.columns(3)
with row1_cols[0]:
    render_kpi_card("Spend", curr_spend, prev_spend, fmt_type="currency", higher_is_better=False, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row1_cols[1]:
    render_kpi_card("Revenue", curr_rev, prev_rev, fmt_type="currency", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row1_cols[2]:
    render_kpi_card("Conversions", curr_conv, prev_conv, fmt_type="integer", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)

row2_cols = st.columns(3)
with row2_cols[0]:
    render_kpi_card("CPA", curr_cpa, prev_cpa, fmt_type="currency_precise", higher_is_better=False, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row2_cols[1]:
    render_kpi_card("ROAS", curr_roas, prev_roas, fmt_type="multiplier", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row2_cols[2]:
    render_kpi_card("ROI", curr_roi, prev_roi, fmt_type="percentage", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)


st.divider()

# ============================================================
# CHANNEL COMPARISON BREAKDOWN
# ============================================================

ch_summary = (
    curr_df.groupby("platform")
    .agg(
        spend=("spend", "sum"),
        revenue=("conversion_value", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        leads=("leads", "sum"),
        conversions=("conversions", "sum")
    )
    .reset_index()
)

ch_summary["ctr"] = (ch_summary["clicks"] / ch_summary["impressions"] * 100).round(2)
ch_summary["cpc"] = (ch_summary["spend"] / ch_summary["clicks"]).round(2)
ch_summary["cpa"] = (ch_summary["spend"] / ch_summary["conversions"]).round(2)
ch_summary["roas"] = (ch_summary["revenue"] / ch_summary["spend"]).round(2)
ch_summary["roi"] = ((ch_summary["revenue"] - ch_summary["spend"]) / ch_summary["spend"] * 100).round(2)

st.subheader("📋 Channel Breakdown Matrix")

st.dataframe(
    ch_summary.style.format({
        "spend": f"{currency_sym}{{:,.2f}}",
        "revenue": f"{currency_sym}{{:,.2f}}",
        "impressions": "{:,.0f}",
        "clicks": "{:,.0f}",
        "leads": "{:,.0f}",
        "conversions": "{:,.0f}",
        "ctr": "{:.2f}%",
        "cpc": f"{currency_sym}{{:,.2f}}",
        "cpa": f"{currency_sym}{{:,.2f}}",
        "roas": "{:.2f}x",
        "roi": "{:,.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# CHARTS: Spend, Revenue, Conversions, ROAS by Channel
# ============================================================

st.subheader("📊 Comparative Channel Visualizations")

c_row1_1, c_row1_2 = st.columns(2)

with c_row1_1:
    fig_spend = px.bar(
        ch_summary,
        x="platform",
        y="spend",
        title="Spend by Channel",
        text_auto=".2s",
        color="platform",
        color_discrete_sequence=["#FF4D5A", "#4F8CFF", "#22C55E"]
    )
    apply_chart_theme(fig_spend, title="Spend by Channel", height=300)
    st.plotly_chart(fig_spend, use_container_width=True)

with c_row1_2:
    fig_pie_spend = px.pie(
        ch_summary,
        values="spend",
        names="platform",
        title="Channel Share of Total Spend",
        hole=0.45,
        color="platform",
        color_discrete_sequence=["#38BDF8", "#FF4D5A", "#10B981"]
    )
    apply_chart_theme(fig_pie_spend, title="Channel Share of Total Spend", height=300)
    st.plotly_chart(fig_pie_spend, use_container_width=True)

c_row2_1, c_row2_2 = st.columns(2)

with c_row2_1:
    fig_rev = px.bar(
        ch_summary,
        x="platform",
        y="revenue",
        title="Revenue by Channel",
        text_auto=".2s",
        color="platform",
        color_discrete_sequence=["#FF4D5A", "#4F8CFF", "#22C55E"]
    )
    apply_chart_theme(fig_rev, title="Revenue by Channel", height=300)
    st.plotly_chart(fig_rev, use_container_width=True)

with c_row2_2:
    fig_pie_conv = px.pie(
        ch_summary,
        values="conversions",
        names="platform",
        title="Channel Share of Total Conversions",
        hole=0.45,
        color="platform",
        color_discrete_sequence=["#38BDF8", "#FF4D5A", "#10B981"]
    )
    apply_chart_theme(fig_pie_conv, title="Channel Share of Total Conversions", height=300)
    st.plotly_chart(fig_pie_conv, use_container_width=True)

st.divider()

# ============================================================
# AI ASSISTANT
# ============================================================

render_ai_assistant("Channel Performance", active_filters=filters)