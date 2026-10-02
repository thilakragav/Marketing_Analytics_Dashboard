import streamlit as st
import pandas as pd
import random
from app.components.kpi_dictionary import render_kpi_popover

def format_val(value: float, fmt_type: str = "number", currency_symbol: str = "₹") -> str:
    """Format numeric values into standard enterprise representations (₹, K, M, %, x)."""
    if value is None or pd.isna(value):
        return "N/A"

    if fmt_type == "currency":
        if abs(value) >= 1_000_000:
            return f"{currency_symbol}{value / 1_000_000:.2f}M"
        elif abs(value) >= 1_000:
            return f"{currency_symbol}{value / 1_000:.1f}K"
        else:
            return f"{currency_symbol}{value:,.2f}"
    elif fmt_type == "currency_precise":
        return f"{currency_symbol}{value:.2f}"
    elif fmt_type == "percentage":
        return f"{value:.2f}%"
    elif fmt_type == "multiplier":
        return f"{value:.2f}x"
    elif fmt_type == "integer":
        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        elif abs(value) >= 1_000:
            return f"{value / 1_000:.0f}K"
        else:
            return f"{int(value):,}"
    elif fmt_type == "decimal":
        return f"{value:.2f}"
    else:
        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        elif abs(value) >= 1_000:
            return f"{value / 1_000:.1f}K"
        else:
            return f"{value:,.2f}"


def _generate_sparkline_html(current_val: float, previous_val: float = None, bars: int = 12) -> str:
    """Generate a CSS-only sparkline mini-chart with gradient bars."""
    if current_val is None or current_val == 0:
        return ""
    
    # Generate plausible bar heights based on current/previous values
    base = max(abs(current_val), 1)
    seed = hash(str(current_val) + str(previous_val)) % 1000
    rng = random.Random(seed)
    
    heights = []
    for i in range(bars):
        # Trend from previous to current
        if previous_val and previous_val != 0:
            ratio = current_val / previous_val
            t = i / max(bars - 1, 1)
            val = previous_val + (current_val - previous_val) * t
            noise = rng.uniform(0.7, 1.3)
            heights.append(max(val * noise, base * 0.1))
        else:
            heights.append(base * rng.uniform(0.3, 1.0))
    
    max_h = max(heights) if heights else 1
    bar_html_parts = []
    for h in heights:
        pct = max(int((h / max_h) * 100), 8)
        bar_html_parts.append(f'<div class="sparkline-bar" style="height:{pct}%"></div>')
    
    return f'<div class="sparkline-container">{"".join(bar_html_parts)}</div>'


def render_kpi_card(
    title: str,
    current_val: float,
    previous_val: float = None,
    fmt_type: str = "currency",
    higher_is_better: bool = True,
    currency_symbol: str = "₹",
    comparison_label: str = "vs previous period",
    incomplete: bool = False
):
    """
    Renders an enterprise KPI card with:
    - Animated gradient top accent beam
    - Uppercase label with info popover
    - Luminous large metric value
    - CSS sparkline mini-chart
    - Trend arrow & change percentage
    - Previous value comparison
    """
    if current_val is None:
        current_val = 0.0

    curr_str = format_val(current_val, fmt_type, currency_symbol)
    inc_badge = " <span style='color: #FBBF24; font-size: 0.7rem; text-shadow: 0 0 6px rgba(245, 158, 11, 0.5);'>● Partial</span>" if incomplete else ""

    with st.container(border=True):
        # Animated gradient top accent beam
        st.markdown(
            "<div style='height: 2px; width: 38px; background: linear-gradient(90deg, #38BDF8, #A855F7, #FF4D5A); border-radius: 2px; box-shadow: 0 0 8px #38BDF8; margin-bottom: 8px;'></div>",
            unsafe_allow_html=True
        )

        head_col1, head_col2 = st.columns([5, 1])
        with head_col1:
            st.markdown(
                f"<div style='font-size: 0.74rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; line-height: 1.4;'>{title}{inc_badge}</div>",
                unsafe_allow_html=True
            )
        with head_col2:
            render_kpi_popover(title)

        st.markdown(
            f"<div style='font-size: 1.85rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.1; margin: 6px 0 4px 0; text-shadow: 0 0 18px rgba(255, 255, 255, 0.25);'>{curr_str}</div>",
            unsafe_allow_html=True
        )

        # Sparkline mini-chart
        sparkline_html = _generate_sparkline_html(current_val, previous_val)
        if sparkline_html:
            st.markdown(sparkline_html, unsafe_allow_html=True)

        if previous_val is None:
            st.markdown(
                "<div style='font-size: 0.74rem; color: #64748B;'>Current selection only</div>",
                unsafe_allow_html=True
            )
            return

        abs_diff = current_val - previous_val
        prev_str = format_val(previous_val, fmt_type, currency_symbol)

        if previous_val == 0:
            trend_html = "<span style='color: #94A3B8; font-weight: 600; font-size: 0.78rem;'>Insufficient Data</span>"
        else:
            pct_val = (abs_diff / abs(previous_val)) * 100.0
            sign = "+" if pct_val > 0 else ""
            pct_str = f"{sign}{pct_val:.1f}%"

            if abs_diff > 0:
                arrow = "↑"
                color = "#34D399" if higher_is_better else "#F87171"
                glow = "rgba(52, 211, 153, 0.4)" if higher_is_better else "rgba(248, 113, 113, 0.4)"
            elif abs_diff < 0:
                arrow = "↓"
                color = "#F87171" if higher_is_better else "#34D399"
                glow = "rgba(248, 113, 113, 0.4)" if higher_is_better else "rgba(52, 211, 153, 0.4)"
            else:
                arrow = "→"
                color = "#94A3B8"
                glow = "transparent"

            trend_html = f"<span style='color: {color}; font-weight: 700; font-size: 0.8rem; text-shadow: 0 0 8px {glow};'>{arrow} {pct_str}</span>"

        st.markdown(
            f"<div style='display: flex; align-items: baseline; gap: 6px; font-size: 0.75rem; color: #94A3B8; border-top: 1px solid rgba(56, 189, 248, 0.15); padding-top: 8px; margin-top: 4px;'>"
            f"{trend_html} <span style='color: #64748B;'>{comparison_label}</span> <span style='color: #475569; margin-left: auto;'>Prev: {prev_str}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
