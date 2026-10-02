import streamlit as st
import pandas as pd
import plotly.express as px
from app.components.theme import apply_enterprise_theme
from app.components.sidebar import render_global_sidebar
from app.components.header import render_global_header
from app.components.charts import apply_chart_theme
from app.components.kpi_dictionary import get_dictionary_dataframe, KPI_DEFINITIONS
from app.utils.currency import get_selected_currency, get_currency_symbol

st.set_page_config(
    page_title="Marketing KPI Dictionary",
    page_icon="📖",
    layout="wide"
)

apply_enterprise_theme()
render_global_sidebar()

render_global_header(
    title="Marketing KPI & Metric Dictionary",
    description="Standardized enterprise business definitions, mathematical formulas, source tables, and attribution methodologies",
    icon="📖"
)

active_code = get_selected_currency()
active_sym = get_currency_symbol()
st.caption(f"🌐 Active Global Reporting Currency: **{active_code} ({active_sym})** (configured in Settings)")

# Search Input
search_query = st.text_input("🔍 Search KPI...", placeholder="Type to filter by metric name, source, or formula (e.g. ROAS, CPA, Spend, Revenue)...")

df_kpi = get_dictionary_dataframe()

if search_query:
    q = search_query.lower()
    df_kpi = df_kpi[
        df_kpi["KPI"].str.lower().str.contains(q)
        | df_kpi["Definition"].str.lower().str.contains(q)
        | df_kpi["Source System"].str.lower().str.contains(q)
        | df_kpi["Formula"].str.lower().str.contains(q)
    ]

st.subheader("📊 Metric System Distribution")
if not df_kpi.empty:
    source_counts = df_kpi["Source System"].value_counts().reset_index()
    source_counts.columns = ["Source System", "Count"]
    fig_kpi_pie = px.pie(
        source_counts,
        values="Count",
        names="Source System",
        title="Metric Definitions by Originating System",
        hole=0.45,
        color_discrete_sequence=["#38BDF8", "#FF4D5A", "#10B981", "#F59E0B", "#818CF8"]
    )
    apply_chart_theme(fig_kpi_pie, title="Metric Definitions by Originating System", height=280)
    st.plotly_chart(fig_kpi_pie, use_container_width=True)

st.subheader("📋 Standardized KPI Directory")
st.dataframe(
    df_kpi,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("📚 Detailed KPI Specifications & Lineage")

for kpi_key, meta in KPI_DEFINITIONS.items():
    with st.expander(f"📌 {meta['name']} — `{meta['formula']}`", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Business Definition:**\n{meta['definition']}")
            st.markdown(f"**Mathematical Formula:** `{meta['formula']}`")
            st.markdown(f"**Aggregation Method:** `{meta['aggregation']}`")
            st.markdown(f"**Unit / Currency:** {meta['currency']}")
        with c2:
            st.markdown(f"**Source System:** {meta['source_system']}")
            st.markdown(f"**Source Table:** `{meta['source_table']}`")
            st.markdown(f"**Source Field(s):** `{meta['source_field']}`")
            st.markdown(f"**Attribution Basis:** {meta['attribution_basis']}")
            st.markdown(f"**Scope & Refresh:** {meta['scope']} • {meta['refresh_cadence']}")
        if meta.get("exclusions"):
            st.caption(f"⚠️ Exclusions: {meta['exclusions']}")
