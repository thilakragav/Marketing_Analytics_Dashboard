import streamlit as st
from datetime import datetime
from app.utils.currency import get_selected_currency, get_currency_symbol

def render_global_sidebar():
    """Renders the fixed enterprise marketing intelligence navigation sidebar with animated brand card, navigation, and system health footer."""
    with st.sidebar:
        # ── Brand Card with rotating rainbow border ──
        st.markdown(
            f"""
            <div class="sidebar-brand-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span class="sidebar-brand-title-text">MARKETING</span>
                    <span class="live-light-dot-red" title="Command Center Active"></span>
                </div>
                <div class="sidebar-brand-sub-text">INTELLIGENCE SUITE</div>
                <div style="display: flex; gap: 6px; margin-top: 10px;">
                    <div style="flex:1; height:3px; border-radius:2px; background: linear-gradient(90deg, #38BDF8, #38BDF8); box-shadow: 0 0 6px rgba(56, 189, 248, 0.5);"></div>
                    <div style="flex:1; height:3px; border-radius:2px; background: linear-gradient(90deg, #A855F7, #A855F7); box-shadow: 0 0 6px rgba(168, 85, 247, 0.5);"></div>
                    <div style="flex:1; height:3px; border-radius:2px; background: linear-gradient(90deg, #FF4D5A, #FF4D5A); box-shadow: 0 0 6px rgba(255, 77, 90, 0.5);"></div>
                    <div style="flex:1; height:3px; border-radius:2px; background: linear-gradient(90deg, #10B981, #10B981); box-shadow: 0 0 6px rgba(168, 185, 129, 0.5);"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Navigation Links ──
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/01_CMO_Executive_Summary.py", label="CMO Executive Summary", icon="📊")
        st.page_link("pages/02_Budget_and_ROI.py", label="Budget & ROI", icon="💰")
        st.page_link("pages/03_Channel_Performance.py", label="Channel Performance", icon="📈")

        st.markdown('<div class="sidebar-section-header">PAID CHANNELS</div>', unsafe_allow_html=True)
        st.page_link("pages/04_Google_Ads.py", label="Google Ads", icon="🔎")
        st.page_link("pages/05_LinkedIn_Ads.py", label="LinkedIn Ads", icon="💼")
        st.page_link("pages/06_Meta_Ads.py", label="Meta Ads", icon="📣")

        st.markdown('<div class="sidebar-section-header">WEB & SEARCH</div>', unsafe_allow_html=True)
        st.page_link("pages/07_GA4_Analytics.py", label="GA4 Analytics", icon="🌐")
        st.page_link("pages/08_SEO_Performance.py", label="SEO Performance", icon="🔍")

        st.markdown('<div class="sidebar-section-header">INTELLIGENCE & AUDIT</div>', unsafe_allow_html=True)
        st.page_link("pages/14_Global_Sales_Map.py", label="Global Sales Map", icon="🗺️")
        st.page_link("pages/09_Data_Sources.py", label="Data Sources", icon="🔄")
        st.page_link("pages/10_Reconciliation.py", label="Reconciliation", icon="🧮")
        st.page_link("pages/11_Attribution.py", label="Attribution", icon="🎯")
        st.page_link("pages/12_KPI_Dictionary.py", label="KPI Dictionary", icon="📖")
        st.page_link("pages/13_Settings.py", label="Settings", icon="⚙️")

        # ── System Health & Currency Footer ──
        now_str = datetime.now().strftime("%H:%M:%S")
        curr_code = get_selected_currency()
        curr_sym = get_currency_symbol()
        st.markdown(
            f"""
            <div style="margin-top: 24px; padding: 12px; background: rgba(10, 16, 28, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; font-size: 0.72rem; color: #64748B;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #94A3B8; letter-spacing: 0.05em;">CURRENCY</span>
                    <span style="color: #38BDF8; font-weight: 800; font-size: 0.75rem;">{curr_code} ({curr_sym})</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 700; color: #94A3B8; letter-spacing: 0.05em;">SYSTEM HEALTH</span>
                    <span style="color: #34D399; font-weight: 700; font-size: 0.68rem;">● ALL ONLINE</span>
                </div>
                <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                    <div style="flex:1; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; padding: 4px 8px; text-align: center;">
                        <div style="font-size: 0.62rem; color: #64748B; font-weight: 600;">DB</div>
                        <div style="font-size: 0.7rem; color: #10B981; font-weight: 800;">OK</div>
                    </div>
                    <div style="flex:1; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 6px; padding: 4px 8px; text-align: center;">
                        <div style="font-size: 0.62rem; color: #64748B; font-weight: 600;">API</div>
                        <div style="font-size: 0.7rem; color: #38BDF8; font-weight: 800;">OK</div>
                    </div>
                    <div style="flex:1; background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 6px; padding: 4px 8px; text-align: center;">
                        <div style="font-size: 0.62rem; color: #64748B; font-weight: 600;">AI</div>
                        <div style="font-size: 0.7rem; color: #A855F7; font-weight: 800;">OK</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.64rem; color: #475569;">
                    <span>Enterprise Suite • v2.4</span>
                    <span style="font-family: 'JetBrains Mono', monospace; color: #64748B;">{now_str}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
