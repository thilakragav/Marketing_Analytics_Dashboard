import streamlit as st
import os
import pandas as pd
import plotly.express as px
from app.components.theme import apply_enterprise_theme
from app.components.sidebar import render_global_sidebar
from app.components.header import render_global_header
from app.components.charts import apply_chart_theme

from app.utils.currency import (
    CURRENCY_CONFIG,
    CURRENCY_OPTIONS,
    get_selected_currency,
    get_currency_symbol,
    get_currency_rate,
    set_selected_currency,
)

st.set_page_config(
    page_title="Platform Settings",
    page_icon="⚙️",
    layout="wide"
)

apply_enterprise_theme()
render_global_sidebar()

render_global_header(
    title="Platform Settings & Preferences",
    description="Display localization, reporting currency, audit tolerances, and credential status",
    icon="⚙️"
)

st.subheader("🌐 Localization & Currency Display")

col1, col2 = st.columns(2)
with col1:
    current_curr = get_selected_currency()
    current_idx = 0
    for idx, opt in enumerate(CURRENCY_OPTIONS):
        if opt.startswith(current_curr):
            current_idx = idx
            break

    def _on_currency_change():
        chosen = st.session_state.get("global_currency_selector")
        if chosen:
            set_selected_currency(chosen)

    selected_currency_label = st.selectbox(
        "Reporting Currency Symbol",
        options=CURRENCY_OPTIONS,
        index=current_idx,
        key="global_currency_selector",
        on_change=_on_currency_change
    )
    if selected_currency_label:
        set_selected_currency(selected_currency_label)

    active_sym = get_currency_symbol()
    active_rate = get_currency_rate()
    if current_curr == "USD":
        st.caption("💵 Base Currency: **USD ($)** • 1 USD = $1.00 USD")
    else:
        st.caption(f"💱 Active Conversion: **1 USD = {active_sym}{active_rate:,.2f} {current_curr}** (Global rate)")

with col2:
    timezone = st.selectbox(
        "Reporting Timezone",
        options=["IST (UTC+05:30)", "UTC", "EST (UTC-05:00)", "PST (UTC-08:00)"],
        index=0
    )

st.divider()

st.subheader("🔑 Live API Secrets & Credentials Status")

credentials = {
    "GA4_PROPERTY_ID": bool(os.getenv("GA4_PROPERTY_ID") or st.secrets.get("GA4_PROPERTY_ID")),
    "GOOGLE_ADS_CUSTOMER_ID": bool(os.getenv("GOOGLE_ADS_CUSTOMER_ID") or st.secrets.get("GOOGLE_ADS_CUSTOMER_ID")),
    "GOOGLE_ADS_DEVELOPER_TOKEN": bool(os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN") or st.secrets.get("GOOGLE_ADS_DEVELOPER_TOKEN")),
    "LINKEDIN_ACCESS_TOKEN": bool(os.getenv("LINKEDIN_ACCESS_TOKEN") or st.secrets.get("LINKEDIN_ACCESS_TOKEN")),
    "META_ACCESS_TOKEN": bool(os.getenv("META_ACCESS_TOKEN") or st.secrets.get("META_ACCESS_TOKEN")),
    "GSC_PROPERTY": bool(os.getenv("GSC_PROPERTY") or st.secrets.get("GSC_PROPERTY")),
    "GROQ_API_KEY": bool(os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")),
    "DB_PASSWORD": bool(os.getenv("DB_PASSWORD") or st.secrets.get("DB_PASSWORD")),
}

status_rows = []
for k, configured in credentials.items():
    status_rows.append({
        "Secret / Environment Key": k,
        "Configured": "✅ Configured" if configured else "⚠️ Not Configured (Using Fallback)",
        "Security Mode": "Masked (Streamlit Secrets / ENV)",
        "Fallback Active": "No" if configured else "Yes (Static / PostgreSQL)"
    })

configured_cnt = sum(1 for c in credentials.values() if c)
unconfigured_cnt = sum(1 for c in credentials.values() if not c)

st.subheader("📊 Integration Readiness Distribution")
fig_settings_pie = px.pie(
    names=["Configured Credentials", "Fallback / Unconfigured"],
    values=[configured_cnt, unconfigured_cnt],
    title="API Key & Integration Readiness Status",
    hole=0.45,
    color_discrete_sequence=["#10B981", "#F59E0B"]
)
apply_chart_theme(fig_settings_pie, title="API Key & Integration Readiness Status", height=280)
st.plotly_chart(fig_settings_pie, use_container_width=True)

st.subheader("📋 Connector Credentials Detailed Status")
st.dataframe(pd.DataFrame(status_rows), use_container_width=True, hide_index=True)

st.divider()

st.subheader("🧹 System Caching & State")
if st.button("Clear Dashboard Cache & Reload"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cache successfully cleared. Reloading...")
    st.rerun()
