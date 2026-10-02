import streamlit as st
import pandas as pd
from datetime import date
from app.services.date_comparison import get_comparison_date_range, check_incomplete_period

def render_filter_bar(
    min_date: date,
    max_date: date,
    channel_options: list[str] = None,
    campaign_options: list[str] = None,
    objective_options: list[str] = None,
    key_prefix: str = "global"
) -> dict:
    """
    Renders premium horizontal filter bar:
    - Title: Dashboard Filters
    - Controls: Date Range, Comparison, Channel, Campaign, Objective
    - Display active filters as pills
    - Reset Filters button
    """
    with st.container(border=True):
        st.markdown(
            """
            <div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);">
                <span class="live-light-dot-cyan"></span> Dashboard Filters & Controls
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([1.5, 1.2, 1.5])

        with col1:
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key=f"{key_prefix}_date_range"
            )

        with col2:
            comparison_mode = st.selectbox(
                "Comparison",
                options=["Previous Period", "Previous Month", "Previous Quarter", "Previous Year", "Custom"],
                index=0,
                key=f"{key_prefix}_comp_mode"
            )

        custom_start = None
        custom_end = None
        if comparison_mode == "Custom":
            with col3:
                custom_range = st.date_input(
                    "Custom Range",
                    value=(min_date, min_date),
                    key=f"{key_prefix}_custom_comp_range"
                )
                if isinstance(custom_range, tuple) and len(custom_range) == 2:
                    custom_start, custom_end = custom_range

        # Parse date range
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range[0], date_range[1]
        elif isinstance(date_range, tuple) and len(date_range) == 1:
            start_date, end_date = date_range[0], date_range[0]
        else:
            start_date, end_date = min_date, max_date

        comp_start, comp_end, comp_label = get_comparison_date_range(
            start_date, end_date, comparison_mode, custom_start, custom_end
        )

        # Secondary row: Channel, Campaign, Objective, Reset
        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns([1.5, 1.5, 1.5, 0.8])

        selected_channels = channel_options or []
        with row2_col1:
            if channel_options:
                selected_channels = st.multiselect(
                    "Channel",
                    options=channel_options,
                    default=channel_options,
                    key=f"{key_prefix}_channels"
                )

        selected_campaigns = []
        with row2_col2:
            if campaign_options:
                selected_campaigns = st.multiselect(
                    "Campaign",
                    options=campaign_options,
                    default=[],
                    placeholder="All Campaigns",
                    key=f"{key_prefix}_campaigns"
                )

        selected_objectives = []
        with row2_col3:
            if objective_options:
                selected_objectives = st.multiselect(
                    "Objective",
                    options=objective_options,
                    default=[],
                    placeholder="All Objectives",
                    key=f"{key_prefix}_objectives"
                )

        with row2_col4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Reset Filters", key=f"{key_prefix}_reset_btn", width="stretch"):
                for k in list(st.session_state.keys()):
                    if k.startswith(key_prefix):
                        del st.session_state[k]
                st.rerun()

    # Active filters display as pills
    pills = [
        f'<div class="filter-pill"><span class="filter-pill-label">DATE</span> {start_date} → {end_date}</div>',
        f'<div class="filter-pill"><span class="filter-pill-label">COMPARISON</span> {comparison_mode}</div>'
    ]

    if channel_options:
        if len(selected_channels) == len(channel_options):
            pills.append('<div class="filter-pill"><span class="filter-pill-label">CHANNEL</span> All Channels</div>')
        else:
            ch_str = ", ".join(selected_channels) if selected_channels else "None"
            pills.append(f'<div class="filter-pill"><span class="filter-pill-label">CHANNEL</span> {ch_str}</div>')

    if selected_campaigns:
        pills.append(f'<div class="filter-pill"><span class="filter-pill-label">CAMPAIGN</span> {len(selected_campaigns)} selected</div>')

    if selected_objectives:
        pills.append(f'<div class="filter-pill"><span class="filter-pill-label">OBJECTIVE</span> {len(selected_objectives)} selected</div>')

    st.markdown(
        f'<div style="margin: 8px 0 16px 0; display: flex; flex-wrap: wrap; gap: 4px;">{"".join(pills)}</div>',
        unsafe_allow_html=True
    )

    is_incomplete = check_incomplete_period(end_date, max_date)
    if is_incomplete:
        st.warning("⚠️ Selected date range extends past latest available dataset. Recent data may be incomplete.")

    return {
        "start_date": pd.Timestamp(start_date),
        "end_date": pd.Timestamp(end_date),
        "comp_start": pd.Timestamp(comp_start),
        "comp_end": pd.Timestamp(comp_end),
        "comp_label": comp_label,
        "comparison_mode": comparison_mode,
        "selected_channels": selected_channels,
        "selected_campaigns": selected_campaigns,
        "selected_objectives": selected_objectives,
        "is_incomplete": is_incomplete
    }
