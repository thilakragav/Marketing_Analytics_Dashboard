import streamlit as st
from datetime import datetime
from app.services.data_sources.manager import get_data_source_manager
from app.utils.currency import get_selected_currency, get_currency_symbol

def render_global_header(
    title: str,
    description: str,
    icon: str = "📊",
    engine = None
):
    """
    Renders ultra-premium enterprise header with:
    - Breadcrumb trail (Home > Current Page)
    - Gradient title with icon bloom
    - Animated status badge with live pulse
    - Timestamp & session clock
    - Luminous gradient divider
    """
    mgr = get_data_source_manager()
    meta = mgr.get_global_freshness_metadata(engine)
    now_str = datetime.now().strftime("%H:%M")

    # Breadcrumb trail
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 6px; font-size: 0.72rem; color: #475569; margin-bottom: 8px; padding-top: 4px;">
            <span style="color: #64748B;">🏠 Home</span>
            <span style="color: #334155;">›</span>
            <span style="color: #94A3B8; font-weight: 600;">{title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3.2, 1.2])

    with col1:
        st.markdown(
            f"""
            <div style="padding-top: 2px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="
                        width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
                        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(168, 85, 247, 0.15));
                        border: 1px solid rgba(56, 189, 248, 0.25);
                        font-size: 1.4rem;
                        filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.5));
                    ">{icon}</div>
                    <div>
                        <h1 style="font-size: 1.65rem; font-weight: 800; margin: 0; padding: 0; line-height: 1.2; letter-spacing: -0.02em; background: linear-gradient(135deg, #FFFFFF 30%, #BAE6FD 70%, #C4B5FD 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                            {title}
                        </h1>
                        <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 4px; font-weight: 400; letter-spacing: -0.01em;">
                            {description}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    curr_code = get_selected_currency()
    curr_sym = get_currency_symbol()

    with col2:
        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 6px;">
                <div class="header-status-badge">
                    <span class="live-light-dot"></span>LIVE INTEGRITY <span style="font-size: 0.72rem; opacity: 0.85;">⚡</span>
                    <span style="margin-left: 8px; border-left: 1px solid rgba(56,189,248,0.3); padding-left: 8px; color: #38BDF8; font-weight: 700;">{curr_code} ({curr_sym})</span>
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 6px;">
                    <div style="font-size: 0.7rem; color: #64748B; font-weight: 500;">
                        Refreshed <strong style="color: #94A3B8;">{meta['last_refresh']}</strong>
                    </div>
                    <div style="font-size: 0.7rem; color: #475569; font-family: 'JetBrains Mono', monospace;">
                        {now_str}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='luminous-divider'></div>", unsafe_allow_html=True)
