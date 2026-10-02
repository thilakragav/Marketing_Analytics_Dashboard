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
from app.components.badges import render_status_badge

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CMO Executive Summary",
    page_icon="📊",
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

# ============================================================
# HEADER
# ============================================================

render_global_header(
    title="CMO Executive Summary",
    description="Executive overview of marketing investment, multi-channel acquisition, revenue returns and portfolio efficiency",
    icon="📊",
    engine=engine
)

if not engine:
    st.error("Database connection is not configured.")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=300)
def load_paid_media():
    query = """
        SELECT
            date,
            campaign_id,
            platform,
            campaign_name,
            objective,
            spend,
            impressions,
            reach,
            clicks,
            leads,
            conversions,
            conversion_value
        FROM paid_media_daily
        ORDER BY date
    """
    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=300)
def load_campaigns():
    query = """
        SELECT
            campaign_id,
            platform,
            account_id,
            campaign_name,
            objective,
            spend,
            impressions,
            reach,
            clicks,
            leads,
            conversions,
            revenue,
            approved_budget,
            target_conversions,
            "target_CPA",
            target_revenue,
            "target_ROAS",
            ctr,
            cpc,
            cpm,
            conversion_rate,
            cpa,
            cpl,
            roas,
            roi,
            budget_utilization
        FROM campaign_performance
        ORDER BY spend DESC
    """
    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)
    return df

try:
    paid_df = load_paid_media()
    campaign_df = load_campaigns()
except Exception as error:
    st.error("Unable to load data from PostgreSQL.")
    st.caption(f"Error: {str(error)}")
    st.stop()

min_date = paid_df["date"].min().date()
max_date = paid_df["date"].max().date()
channels = sorted(paid_df["platform"].unique().tolist())
campaign_list = sorted(paid_df["campaign_name"].dropna().unique().tolist())
objectives_list = sorted(paid_df["objective"].dropna().unique().tolist())

# ============================================================
# FILTER BAR WITH DATE COMPARISON
# ============================================================

filters = render_filter_bar(
    min_date=min_date,
    max_date=max_date,
    channel_options=channels,
    campaign_options=campaign_list,
    objective_options=objectives_list,
    key_prefix="cmo"
)

# Apply filters for current period
curr_df = paid_df[
    (paid_df["date"] >= filters["start_date"])
    & (paid_df["date"] <= filters["end_date"])
    & (paid_df["platform"].isin(filters["selected_channels"]))
]
if filters["selected_campaigns"]:
    curr_df = curr_df[curr_df["campaign_name"].isin(filters["selected_campaigns"])]
if filters["selected_objectives"]:
    curr_df = curr_df[curr_df["objective"].isin(filters["selected_objectives"])]

# Apply filters for comparison period
prev_df = paid_df[
    (paid_df["date"] >= filters["comp_start"])
    & (paid_df["date"] <= filters["comp_end"])
    & (paid_df["platform"].isin(filters["selected_channels"]))
]
if filters["selected_campaigns"]:
    prev_df = prev_df[prev_df["campaign_name"].isin(filters["selected_campaigns"])]
if filters["selected_objectives"]:
    prev_df = prev_df[prev_df["objective"].isin(filters["selected_objectives"])]

if curr_df.empty:
    st.warning("No data is available for the selected filters.")
    st.stop()

# ============================================================
# KPI CALCULATIONS
# ============================================================

curr_spend = curr_df["spend"].sum()
prev_spend = prev_df["spend"].sum() if not prev_df.empty else 0.0

curr_rev = curr_df["conversion_value"].sum()
prev_rev = prev_df["conversion_value"].sum() if not prev_df.empty else 0.0

curr_conv = curr_df["conversions"].sum()
prev_conv = prev_df["conversions"].sum() if not prev_df.empty else 0.0

curr_roas = (curr_rev / curr_spend) if curr_spend > 0 else 0.0
prev_roas = (prev_rev / prev_spend) if prev_spend > 0 else 0.0

curr_roi = ((curr_rev - curr_spend) / curr_spend * 100) if curr_spend > 0 else 0.0
prev_roi = ((prev_rev - prev_spend) / prev_spend * 100) if prev_spend > 0 else 0.0

curr_cpa = (curr_spend / curr_conv) if curr_conv > 0 else 0.0
prev_cpa = (prev_spend / prev_conv) if prev_conv > 0 else 0.0

currency_sym = st.session_state.get("currency_symbol", "$")
comp_lbl = filters["comp_label"]
is_inc = filters["is_incomplete"]

# ============================================================
# TOP EXECUTIVE ROW: Spend, Revenue, Conversions, ROAS, ROI, CPA
# ============================================================

st.subheader("Executive Performance Scorecard")

row1_cols = st.columns(3)
with row1_cols[0]:
    render_kpi_card("Spend", curr_spend, prev_spend, fmt_type="currency", higher_is_better=False, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row1_cols[1]:
    render_kpi_card("Revenue", curr_rev, prev_rev, fmt_type="currency", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row1_cols[2]:
    render_kpi_card("Conversions", curr_conv, prev_conv, fmt_type="integer", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)

row2_cols = st.columns(3)
with row2_cols[0]:
    render_kpi_card("ROAS", curr_roas, prev_roas, fmt_type="multiplier", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row2_cols[1]:
    render_kpi_card("ROI", curr_roi, prev_roi, fmt_type="percentage", higher_is_better=True, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)
with row2_cols[2]:
    render_kpi_card("CPA", curr_cpa, prev_cpa, fmt_type="currency_precise", higher_is_better=False, currency_symbol=currency_sym, comparison_label=comp_lbl, incomplete=is_inc)


st.divider()

# ============================================================
# 2-COLUMN PERFORMANCE OVERVIEW (TREND LEFT, ROAS RIGHT)
# ============================================================

col_trend, col_roas = st.columns(2)

with col_trend:
    st.subheader("📈 Spend vs Revenue Performance Trend")
    daily_summary = (
        curr_df.groupby("date")
        .agg(spend=("spend", "sum"), revenue=("conversion_value", "sum"), conversions=("conversions", "sum"))
        .reset_index()
    )
    fig_daily = px.line(
        daily_summary,
        x="date",
        y=["spend", "revenue"],
        title="Daily Spend vs Attributed Revenue",
        color_discrete_map={"spend": "#FF4D5A", "revenue": "#22C55E"}
    )
    apply_chart_theme(fig_daily, title="Daily Spend vs Attributed Revenue", height=320)
    st.plotly_chart(fig_daily, use_container_width=True)

with col_roas:
    st.subheader("🎯 Channel Efficiency (ROAS)")
    channel_summary = (
        curr_df.groupby("platform")
        .agg(
            spend=("spend", "sum"),
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
            leads=("leads", "sum"),
            conversions=("conversions", "sum"),
            revenue=("conversion_value", "sum")
        )
        .reset_index()
    )
    channel_summary["roas"] = (channel_summary["revenue"] / channel_summary["spend"]).round(2)
    channel_summary["cpa"] = (channel_summary["spend"] / channel_summary["conversions"]).round(2)
    channel_summary["ctr"] = (channel_summary["clicks"] / channel_summary["impressions"] * 100).round(2)
    channel_summary["roi"] = ((channel_summary["revenue"] - channel_summary["spend"]) / channel_summary["spend"] * 100).round(2)

    fig_roas = px.bar(
        channel_summary,
        x="platform",
        y="roas",
        title="Return on Ad Spend (ROAS) by Channel",
        text_auto=".2f",
        color="platform",
        color_discrete_sequence=["#4F8CFF", "#FF4D5A", "#22C55E"]
    )
    apply_chart_theme(fig_roas, title="Return on Ad Spend (ROAS) by Channel", height=320)
    st.plotly_chart(fig_roas, use_container_width=True)

# ============================================================
# CHANNEL PERFORMANCE BREAKDOWN
# ============================================================

st.subheader("🌐 Channel Performance Breakdown")

c_col1, c_col2 = st.columns([1.3, 1.1])

with c_col1:
    fig_channel_comp = px.bar(
        channel_summary,
        y="platform",
        x=["spend", "revenue"],
        barmode="group",
        orientation="h",
        title="Spend vs Revenue by Marketing Channel",
        color_discrete_map={"spend": "#FF4D5A", "revenue": "#22C55E"}
    )
    apply_chart_theme(fig_channel_comp, title="Spend vs Revenue by Marketing Channel", height=280)
    st.plotly_chart(fig_channel_comp, use_container_width=True)

with c_col2:
    fig_cmo_pie = px.pie(
        channel_summary,
        values="revenue",
        names="platform",
        title="Revenue Contribution Share",
        hole=0.45,
        color="platform",
        color_discrete_sequence=["#38BDF8", "#FF4D5A", "#10B981"]
    )
    apply_chart_theme(fig_cmo_pie, title="Revenue Contribution Share", height=280)
    st.plotly_chart(fig_cmo_pie, use_container_width=True)

st.dataframe(
    channel_summary.style.format({
        "spend": f"{currency_sym}{{:,.2f}}",
        "revenue": f"{currency_sym}{{:,.2f}}",
        "impressions": "{:,.0f}",
        "clicks": "{:,.0f}",
        "leads": "{:,.0f}",
        "conversions": "{:,.0f}",
        "roas": "{:.2f}x",
        "cpa": f"{currency_sym}{{:,.2f}}",
        "ctr": "{:.2f}%",
        "roi": "{:,.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# CAMPAIGN PERFORMANCE TABLE
# ============================================================

st.subheader("🎯 Campaign Performance")

campaign_display = campaign_df[campaign_df["platform"].isin(filters["selected_channels"])].copy()

campaign_display["budget_status"] = campaign_display["budget_utilization"].apply(
    lambda x: "🔴 Over Budget" if x >= 100 else ("🟡 Near Budget" if x >= 80 else "🟢 On Track")
)
campaign_display["target_status"] = campaign_display.apply(
    lambda row: "🟢 Target Met" if row["roas"] >= row["target_ROAS"] else "🔴 Below Target",
    axis=1
)

formatted_campaign = campaign_display[
    [
        "campaign_id",
        "platform",
        "campaign_name",
        "objective",
        "spend",
        "revenue",
        "conversions",
        "approved_budget",
        "budget_utilization",
        "roas",
        "roi",
        "budget_status",
        "target_status"
    ]
].sort_values("spend", ascending=False)

st.dataframe(
    formatted_campaign.style.format({
        "spend": f"{currency_sym}{{:,.2f}}",
        "revenue": f"{currency_sym}{{:,.2f}}",
        "approved_budget": f"{currency_sym}{{:,.2f}}",
        "conversions": "{:,.0f}",
        "budget_utilization": "{:.1f}%",
        "roas": "{:.2f}x",
        "roi": "{:,.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# AI ASSISTANT WITH FILTER AWARENESS
# ============================================================

render_ai_assistant("CMO Executive Summary", active_filters=filters)