import base64
from pathlib import Path

import streamlit as st

# Background image shown behind every page (Home + all pages in /pages)
_BACKGROUND_IMAGE = Path(__file__).resolve().parent.parent / "assets" / "dashboard_background.svg"
_TRANSPARENT_PIXEL = (
    "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)


@st.cache_data(show_spinner=False)
def _background_image_uri() -> str:
    """Return the dashboard background as a data URI (falls back to nothing if missing)."""
    try:
        encoded = base64.b64encode(_BACKGROUND_IMAGE.read_bytes()).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}"
    except OSError:
        return _TRANSPARENT_PIXEL


def apply_enterprise_theme():
    """
    Injects high-end dark enterprise SaaS luxury styling:
    - Custom Google Fonts (Plus Jakarta Sans & JetBrains Mono)
    - Atmospheric multi-point ambient mesh lighting
    - Luminous double-rimmed cards with laser top-accent beams
    - Card-styled st.metric widgets with glowing metrics and delta badges
    - Luminous color-coded outlines for all buttons and controls
    - Glassmorphic alerts with vertical glowing status bars
    - Ultra-sleek sidebar navigation with glowing active/hover states
    - Frosted-glass dataframes and Plotly chart wrappers
    """
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

        <style>
        :root {
            --bg-canvas: #060911;
            --bg-surface-1: #0A0F1D;
            --bg-surface-2: #0F172A;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-hover: rgba(22, 34, 60, 0.85);
            
            --border-dim: rgba(56, 189, 248, 0.18);
            --border-medium: rgba(56, 189, 248, 0.32);
            --border-glow: rgba(56, 189, 248, 0.65);
            
            --cyan-glow: #38BDF8;
            --cyan-dim: rgba(56, 189, 248, 0.15);
            --crimson-glow: #FF4D5A;
            --crimson-dim: rgba(255, 77, 90, 0.15);
            --emerald-glow: #10B981;
            --emerald-dim: rgba(16, 185, 129, 0.15);
            --amber-glow: #F59E0B;
            --amber-dim: rgba(245, 158, 11, 0.15);
            --violet-glow: #A855F7;
            --violet-dim: rgba(168, 85, 247, 0.15);
            --indigo-glow: #818CF8;

            --text-heading: #FFFFFF;
            --text-body: #E2E8F0;
            --text-muted: #94A3B8;
            --text-subtle: #64748B;
            
            --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        /* ========================================================
           GLOBAL APP CANVAS & MULTI-POINT AMBIENT LIGHTING
           ======================================================== */
        html, body, [class*="css"] {
            font-family: var(--font-main) !important;
        }

        .stApp {
            background-color: #080C16 !important;
            background-image: 
                /* Top soft ambient light glow */
                radial-gradient(ellipse 70% 35% at 50% -5%, rgba(38, 80, 138, 0.28) 0%, transparent 70%),
                /* Subtle top-right purple tech glow */
                radial-gradient(ellipse 45% 30% at 95% 5%, rgba(99, 45, 140, 0.16) 0%, transparent 65%),
                /* Subtle bottom-left cyan tech glow */
                radial-gradient(ellipse 45% 30% at 5% 95%, rgba(14, 116, 144, 0.12) 0%, transparent 65%),
                /* Architectural precision micro-grid */
                linear-gradient(to right, rgba(56, 189, 248, 0.035) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(56, 189, 248, 0.035) 1px, transparent 1px),
                /* Soft dark veil so text stays readable over the image */
                linear-gradient(rgba(6, 9, 17, 0.38), rgba(6, 9, 17, 0.38)),
                /* Background image: glowing marketing trend lines & bars */
                url("__BG_IMAGE__") !important;
            background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px, 100% 100%, cover !important;
            background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, center center !important;
            background-repeat: repeat, repeat, repeat, repeat, repeat, no-repeat, no-repeat !important;
            background-attachment: fixed !important;
            color: var(--text-body) !important;
        }

        /* Custom Cyber Neon Scrollbars */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }
        ::-webkit-scrollbar-track {
            background: #060911;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(56, 189, 248, 0.35);
            border-radius: 4px;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
            transition: all 0.2s ease;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(56, 189, 248, 0.65);
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.85);
        }

        /* Typography Hierarchy */
        h1 {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        h2 {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
        }
        h3 {
            color: #F8FAFC !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        p, span, label {
            letter-spacing: -0.01em;
        }

        /* ========================================================
           STREAMLIT METRIC CARDS (st.metric)
           Transforms standard metrics into luminous luxury cards
           ======================================================== */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(16, 24, 40, 0.85) 0%, rgba(10, 16, 28, 0.95) 100%) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.26) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            box-shadow: 0 4px 22px rgba(0, 0, 0, 0.5), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.1), 
                        0 0 14px rgba(56, 189, 248, 0.08) !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            backdrop-filter: blur(12px) !important;
        }
        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 10%;
            right: 10%;
            height: 1.5px;
            background: linear-gradient(90deg, transparent, #38BDF8 40%, #FF4D5A 60%, transparent);
            box-shadow: 0 0 8px #38BDF8;
            pointer-events: none;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #38BDF8 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65), 
                        0 0 22px rgba(56, 189, 248, 0.35), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
            transform: translateY(-2px) !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-size: 0.74rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            line-height: 1.3 !important;
        }
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 1.75rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            text-shadow: 0 0 18px rgba(255, 255, 255, 0.22) !important;
            margin: 4px 0 6px 0 !important;
        }
        div[data-testid="stMetricDelta"] {
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 4px !important;
        }

        /* ========================================================
           STREAMLIT ALERTS (Warning, Info, Success, Error)
           Glassmorphic cards with luminous vertical indicator bars
           ======================================================== */
        div[data-testid="stAlert"] {
            background: rgba(14, 20, 33, 0.88) !important;
            backdrop-filter: blur(14px) !important;
            border-radius: 12px !important;
            padding: 14px 20px !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5) !important;
            margin: 12px 0 !important;
        }
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {
            color: #F8FAFC !important;
            font-size: 0.9rem !important;
        }
        /* Warning: Luminous Amber Gold */
        div[data-testid="stAlert"]:has([data-testid="stNotificationContentWarning"]) {
            border: 1.5px solid rgba(245, 158, 11, 0.5) !important;
            border-left: 5px solid #F59E0B !important;
            box-shadow: 0 0 22px rgba(245, 158, 11, 0.25), inset 0 0 12px rgba(245, 158, 11, 0.08) !important;
        }
        /* Info: Luminous Sapphire Cyan */
        div[data-testid="stAlert"]:has([data-testid="stNotificationContentInfo"]) {
            border: 1.5px solid rgba(56, 189, 248, 0.5) !important;
            border-left: 5px solid #38BDF8 !important;
            box-shadow: 0 0 22px rgba(56, 189, 248, 0.25), inset 0 0 12px rgba(56, 189, 248, 0.08) !important;
        }
        /* Success: Luminous Emerald Green */
        div[data-testid="stAlert"]:has([data-testid="stNotificationContentSuccess"]) {
            border: 1.5px solid rgba(16, 185, 129, 0.5) !important;
            border-left: 5px solid #10B981 !important;
            box-shadow: 0 0 22px rgba(16, 185, 129, 0.25), inset 0 0 12px rgba(16, 185, 129, 0.08) !important;
        }
        /* Error: Luminous Crimson Red */
        div[data-testid="stAlert"]:has([data-testid="stNotificationContentError"]) {
            border: 1.5px solid rgba(239, 68, 68, 0.5) !important;
            border-left: 5px solid #EF4444 !important;
            box-shadow: 0 0 22px rgba(239, 68, 68, 0.25), inset 0 0 12px rgba(239, 68, 68, 0.08) !important;
        }

        /* ========================================================
           GLOBAL SIDEBAR: LUXURY BRAND CARD & GLOWING NAV LINKS
           ======================================================== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #090E1A 0%, #060912 100%) !important;
            border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important;
            box-shadow: 4px 0 28px rgba(0, 0, 0, 0.7), inset -1px 0 0 rgba(56, 189, 248, 0.15) !important;
        }

        /* Brand Card in Sidebar */
        .sidebar-brand-card {
            background: linear-gradient(145deg, rgba(28, 16, 32, 0.9) 0%, rgba(13, 19, 36, 0.95) 100%);
            border: 1.5px solid rgba(255, 77, 90, 0.55);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 22px rgba(0, 0, 0, 0.55), 0 0 18px rgba(255, 77, 90, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.15);
            position: relative;
            overflow: hidden;
        }
        .sidebar-brand-card::after {
            content: "";
            position: absolute;
            top: 0;
            left: 15%;
            right: 15%;
            height: 1.5px;
            background: linear-gradient(90deg, transparent, #FF4D5A 40%, #38BDF8 60%, transparent);
            box-shadow: 0 0 8px #FF4D5A;
        }
        .sidebar-brand-title-text {
            font-size: 1.15rem;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: 0.14em;
            text-shadow: 0 0 14px rgba(255, 77, 90, 0.55);
        }
        .sidebar-brand-sub-text {
            font-size: 0.72rem;
            font-weight: 800;
            color: #38BDF8;
            letter-spacing: 0.24em;
            margin-top: 4px;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.45);
        }

        /* Sidebar Section Header Capsules */
        .sidebar-section-header {
            font-size: 0.68rem;
            font-weight: 800;
            color: #38BDF8;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-top: 18px;
            margin-bottom: 8px;
            padding: 4px 12px;
            display: inline-block;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 20px;
            background: rgba(56, 189, 248, 0.08);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
        }

        /* Sidebar Links: Every link with an explicit elegant colored outline */
        div[data-testid="stSidebar"] a {
            border: 1px solid rgba(56, 189, 248, 0.22) !important;
            background: linear-gradient(135deg, rgba(16, 24, 40, 0.7) 0%, rgba(10, 16, 28, 0.8) 100%) !important;
            border-radius: 9px !important;
            padding: 9px 13px !important;
            color: #94A3B8 !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
            text-decoration: none !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            margin-bottom: 6px !important;
            display: flex !important;
            align-items: center !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
        }

        div[data-testid="stSidebar"] a:hover {
            border-color: #38BDF8 !important;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.18) 0%, rgba(18, 30, 52, 0.88) 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.4), inset 0 0 10px rgba(56, 189, 248, 0.18) !important;
            transform: translateX(4px) !important;
        }

        div[data-testid="stSidebar"] a[aria-current="page"] {
            border: 1.5px solid #FF4D5A !important;
            background: linear-gradient(90deg, rgba(255, 77, 90, 0.24) 0%, rgba(255, 77, 90, 0.06) 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-radius: 9px !important;
            box-shadow: 0 0 20px rgba(255, 77, 90, 0.42), inset 0 0 12px rgba(255, 77, 90, 0.22) !important;
            transform: translateX(4px) !important;
        }

        /* ========================================================
           BUTTONS: VIVID ELEGANT COLORS & LUMINOUS COLORED OUTLINES
           ======================================================== */
        /* Primary Action Buttons (e.g. Ask AI, Main triggers) */
        button[kind="primary"] {
            background: linear-gradient(135deg, #FF4D5A 0%, #D92338 100%) !important;
            border: 1.5px solid #FF7582 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-radius: 9px !important;
            box-shadow: 0 4px 16px rgba(255, 77, 90, 0.45), 0 0 12px rgba(255, 77, 90, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.35) !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        button[kind="primary"]:hover {
            border-color: #FFA5AE !important;
            box-shadow: 0 6px 26px rgba(255, 77, 90, 0.75), 0 0 20px rgba(255, 77, 90, 0.55), inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        button[kind="primary"]:active {
            transform: translateY(0px) scale(0.99) !important;
        }

        /* Standard / Secondary Buttons: Sapphire Cyan Colored Outline */
        button[kind="secondary"],
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, rgba(14, 28, 52, 0.9) 0%, rgba(9, 18, 34, 0.95) 100%) !important;
            border: 1.5px solid #38BDF8 !important;
            color: #38BDF8 !important;
            font-weight: 700 !important;
            border-radius: 9px !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45), 0 0 12px rgba(56, 189, 248, 0.22), inset 0 1px 0 rgba(56, 189, 248, 0.2) !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        button[kind="secondary"]:hover,
        div[data-testid="stButton"] > button:hover {
            border-color: #7DD3FC !important;
            color: #FFFFFF !important;
            background: linear-gradient(135deg, rgba(22, 48, 88, 0.95) 0%, rgba(14, 28, 52, 0.98) 100%) !important;
            box-shadow: 0 6px 22px rgba(56, 189, 248, 0.5), 0 0 18px rgba(56, 189, 248, 0.35), inset 0 0 10px rgba(56, 189, 248, 0.3) !important;
            transform: translateY(-2px) !important;
        }
        button[kind="secondary"]:active,
        div[data-testid="stButton"] > button:active {
            transform: translateY(0px) scale(0.99) !important;
        }

        /* Specific Reset Filter Button with Amber Gold Outline */
        button:has(p:contains("Reset")),
        div[data-testid="stButton"]:has(button:contains("Reset")) button {
            background: linear-gradient(135deg, rgba(48, 30, 10, 0.9) 0%, rgba(26, 16, 6, 0.95) 100%) !important;
            border: 1.5px solid #F59E0B !important;
            color: #FBBF24 !important;
            font-weight: 700 !important;
            box-shadow: 0 0 14px rgba(245, 158, 11, 0.28), inset 0 1px 0 rgba(245, 158, 11, 0.2) !important;
        }
        button:has(p:contains("Reset")):hover,
        div[data-testid="stButton"]:has(button:contains("Reset")) button:hover {
            border-color: #FCD34D !important;
            color: #FFFFFF !important;
            background: linear-gradient(135deg, rgba(68, 42, 14, 0.95) 0%, rgba(38, 22, 8, 0.98) 100%) !important;
            box-shadow: 0 0 24px rgba(245, 158, 11, 0.6), inset 0 0 10px rgba(245, 158, 11, 0.3) !important;
            transform: translateY(-2px) !important;
        }

        /* Quick Questions: Highest ROAS Button with Emerald Green Outline */
        button:has(p:contains("Highest ROAS")),
        div[data-testid="stButton"]:has(button:contains("Highest ROAS")) button {
            border: 1.5px solid #10B981 !important;
            color: #34D399 !important;
            background: linear-gradient(135deg, rgba(10, 38, 26, 0.88) 0%, rgba(6, 22, 16, 0.95) 100%) !important;
            box-shadow: 0 0 14px rgba(16, 185, 129, 0.25) !important;
        }
        button:has(p:contains("Highest ROAS")):hover,
        div[data-testid="stButton"]:has(button:contains("Highest ROAS")) button:hover {
            border-color: #6EE7B7 !important;
            color: #FFFFFF !important;
            background: linear-gradient(135deg, rgba(16, 54, 38, 0.95) 0%, rgba(10, 38, 26, 0.98) 100%) !important;
            box-shadow: 0 0 24px rgba(16, 185, 129, 0.55), inset 0 0 10px rgba(16, 185, 129, 0.3) !important;
            transform: translateY(-2px) !important;
        }

        /* Quick Questions: Top Performing Button with Royal Violet Outline */
        button:has(p:contains("Top Performing")),
        div[data-testid="stButton"]:has(button:contains("Top Performing")) button {
            border: 1.5px solid #A855F7 !important;
            color: #C084FC !important;
            background: linear-gradient(135deg, rgba(35, 16, 56, 0.88) 0%, rgba(19, 9, 32, 0.95) 100%) !important;
            box-shadow: 0 0 14px rgba(168, 85, 247, 0.25) !important;
        }
        button:has(p:contains("Top Performing")):hover,
        div[data-testid="stButton"]:has(button:contains("Top Performing")) button:hover {
            border-color: #D8B4FE !important;
            color: #FFFFFF !important;
            background: linear-gradient(135deg, rgba(50, 24, 80, 0.95) 0%, rgba(35, 16, 56, 0.98) 100%) !important;
            box-shadow: 0 0 24px rgba(168, 85, 247, 0.55), inset 0 0 10px rgba(168, 85, 247, 0.3) !important;
            transform: translateY(-2px) !important;
        }

        /* Download Buttons: Vibrant Indigo Outline */
        div[data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, rgba(24, 26, 60, 0.9) 0%, rgba(14, 16, 38, 0.95) 100%) !important;
            border: 1.5px solid #818CF8 !important;
            color: #A5B4FC !important;
            font-weight: 700 !important;
            border-radius: 9px !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45), 0 0 12px rgba(129, 140, 248, 0.25) !important;
            transition: all 0.22s ease !important;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            border-color: #C7D2FE !important;
            color: #FFFFFF !important;
            box-shadow: 0 6px 22px rgba(129, 140, 248, 0.55), 0 0 18px rgba(129, 140, 248, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        /* ========================================================
           CONTAINERS WITH BORDER=TRUE: DOUBLE-RIM RIMLIGHTING
           ======================================================== */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background: linear-gradient(145deg, rgba(16, 24, 40, 0.8) 0%, rgba(11, 17, 30, 0.92) 100%) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.26) !important;
            border-radius: 12px !important;
            padding: 18px 20px !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.08),
                        0 0 14px rgba(56, 189, 248, 0.06) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            position: relative !important;
            backdrop-filter: blur(12px) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div::before {
            content: "";
            position: absolute;
            top: 0;
            left: 10%;
            right: 10%;
            height: 1.5px;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.8), rgba(255, 77, 90, 0.7), transparent);
            pointer-events: none;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
            border-color: rgba(56, 189, 248, 0.55) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65), 
                        0 0 20px rgba(56, 189, 248, 0.25), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        }

        /* KPI Custom Container */
        .kpi-container {
            background: linear-gradient(145deg, rgba(18, 24, 38, 0.9) 0%, rgba(13, 19, 31, 0.95) 100%) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.28) !important;
            border-radius: 12px !important;
            padding: 16px 18px !important;
            box-shadow: 0 4px 22px rgba(0, 0, 0, 0.5), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.08), 
                        0 0 12px rgba(56, 189, 248, 0.08) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            position: relative !important;
            overflow: hidden !important;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .kpi-container::before {
            content: "";
            position: absolute;
            top: 0;
            left: 10%;
            right: 10%;
            height: 1.5px;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.8), rgba(255, 77, 90, 0.7), transparent);
            pointer-events: none;
        }
        .kpi-container:hover {
            border-color: #38BDF8 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65), 
                        0 0 22px rgba(56, 189, 248, 0.32), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            transform: translateY(-2px) !important;
        }

        /* ========================================================
           PLOTLY CHARTS CONTAINER
           ======================================================== */
        div[data-testid="stPlotlyChart"] {
            border: 1.5px solid rgba(56, 189, 248, 0.26) !important;
            border-radius: 12px !important;
            padding: 8px !important;
            background: linear-gradient(145deg, rgba(16, 23, 38, 0.85) 0%, rgba(10, 16, 27, 0.95) 100%) !important;
            box-shadow: 0 4px 22px rgba(0, 0, 0, 0.5), 0 0 14px rgba(56, 189, 248, 0.08) !important;
            transition: all 0.25s ease !important;
            position: relative !important;
            overflow: hidden !important;
        }
        div[data-testid="stPlotlyChart"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 10%;
            right: 10%;
            height: 1.5px;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.7) 50%, transparent);
            pointer-events: none;
        }
        div[data-testid="stPlotlyChart"]:hover {
            border-color: rgba(56, 189, 248, 0.55) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.65), 0 0 20px rgba(56, 189, 248, 0.22) !important;
        }

        /* ========================================================
           FORM CONTROLS: INPUTS, SELECTS, MULTISELECT, DATEPICKER
           ======================================================== */
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"],
        div[data-testid="stMultiSelect"] div[data-baseweb="select"],
        div[data-testid="stDateInput"] input {
            background-color: #0A111E !important;
            border: 1.5px solid rgba(56, 189, 248, 0.32) !important;
            color: #F8FAFC !important;
            border-radius: 9px !important;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5), 0 0 8px rgba(56, 189, 248, 0.08) !important;
            transition: all 0.22s ease !important;
        }
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within,
        div[data-testid="stMultiSelect"] div[data-baseweb="select"]:focus-within,
        div[data-testid="stDateInput"] input:focus {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.35), 0 0 18px rgba(56, 189, 248, 0.45) !important;
        }

        /* Multiselect Selected Pills */
        div[data-baseweb="tag"] {
            background: rgba(56, 189, 248, 0.18) !important;
            border: 1px solid #38BDF8 !important;
            color: #F0F9FF !important;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.25) !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }

        /* Dropdown Menus & Popovers */
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"] {
            border: 1.5px solid rgba(56, 189, 248, 0.45) !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85), 0 0 22px rgba(56, 189, 248, 0.28) !important;
            background: #090F1C !important;
            border-radius: 12px !important;
        }

        /* ========================================================
           DATAFRAMES & TABLES
           ======================================================== */
        div[data-testid="stDataFrame"] {
            border: 1.5px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            background-color: rgba(18, 24, 38, 0.9) !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5), 0 0 14px rgba(56, 189, 248, 0.1) !important;
        }

        /* Expanders: Glowing Violet Outline */
        div[data-testid="stExpander"] {
            border: 1.5px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 12px !important;
            background: linear-gradient(145deg, rgba(23, 18, 43, 0.6) 0%, rgba(13, 19, 36, 0.75) 100%) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45), 0 0 16px rgba(168, 85, 247, 0.18) !important;
            transition: all 0.22s ease !important;
        }
        div[data-testid="stExpander"]:hover {
            border-color: #A855F7 !important;
            box-shadow: 0 6px 26px rgba(168, 85, 247, 0.35) !important;
        }

        /* Tabs Outline */
        button[data-baseweb="tab"] {
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 8px 8px 0 0 !important;
            margin-right: 6px !important;
            padding: 9px 20px !important;
            background: rgba(14, 20, 34, 0.7) !important;
            color: #94A3B8 !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        button[data-baseweb="tab"]:hover {
            border-color: #38BDF8 !important;
            color: #FFFFFF !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            border: 1.5px solid #38BDF8 !important;
            border-bottom: 2px solid #38BDF8 !important;
            background: rgba(56, 189, 248, 0.16) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            box-shadow: 0 -4px 16px rgba(56, 189, 248, 0.25) !important;
        }

        /* Sliders: Glowing Cyan Handle */
        div[data-testid="stSlider"] div[role="slider"] {
            background-color: #38BDF8 !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 0 12px #38BDF8, 0 0 4px #FFFFFF !important;
        }

        /* Code Blocks */
        div[data-testid="stCodeBlock"] {
            border: 1.5px solid rgba(56, 189, 248, 0.35) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.15) !important;
            font-family: var(--font-mono) !important;
        }

        /* Filter Pills */
        .filter-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, rgba(18, 24, 38, 0.95) 0%, rgba(13, 19, 31, 0.95) 100%);
            color: #F8FAFC;
            border: 1.5px solid rgba(56, 189, 248, 0.35);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 6px;
            margin-bottom: 6px;
            backdrop-filter: blur(8px);
            transition: all 0.2s ease;
        }
        .filter-pill:hover {
            border-color: #38BDF8;
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }
        .filter-pill-label {
            color: #38BDF8;
            font-size: 0.72rem;
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 0.06em;
            margin-right: 4px;
        }

        /* Pulsing LED Indicators */
        @keyframes pulse-emerald {
            0%, 100% {
                box-shadow: 0 0 4px #10B981, 0 0 10px rgba(16, 185, 129, 0.6);
                opacity: 1;
            }
            50% {
                box-shadow: 0 0 8px #10B981, 0 0 18px rgba(16, 185, 129, 0.9);
                opacity: 0.8;
            }
        }
        @keyframes pulse-red {
            0%, 100% {
                box-shadow: 0 0 4px #FF4D5A, 0 0 10px rgba(255, 77, 90, 0.6);
                opacity: 1;
            }
            50% {
                box-shadow: 0 0 8px #FF4D5A, 0 0 18px rgba(255, 77, 90, 0.9);
                opacity: 0.8;
            }
        }
        @keyframes pulse-cyan {
            0%, 100% {
                box-shadow: 0 0 4px #38BDF8, 0 0 10px rgba(56, 189, 248, 0.6);
            }
            50% {
                box-shadow: 0 0 8px #38BDF8, 0 0 18px rgba(56, 189, 248, 0.9);
            }
        }

        .live-light-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10B981;
            animation: pulse-emerald 2s infinite ease-in-out;
            margin-right: 6px;
            vertical-align: middle;
        }
        .live-light-dot-red {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #FF4D5A;
            animation: pulse-red 2s infinite ease-in-out;
            margin-right: 6px;
            vertical-align: middle;
        }
        .live-light-dot-cyan {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #38BDF8;
            animation: pulse-cyan 2s infinite ease-in-out;
            margin-right: 6px;
            vertical-align: middle;
        }

        /* Luminous Header Styling */
        .page-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0 14px 0;
            margin-bottom: 12px;
        }

        .luminous-divider {
            height: 1.5px;
            background: linear-gradient(90deg, transparent 0%, rgba(56, 189, 248, 0.8) 25%, rgba(255, 77, 90, 0.8) 75%, transparent 100%);
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.6);
            margin: 12px 0 20px 0;
        }

        .header-status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.14) !important;
            border: 1.5px solid rgba(16, 185, 129, 0.5) !important;
            color: #34D399 !important;
            padding: 5px 14px !important;
            border-radius: 20px !important;
            font-size: 0.75rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.08em !important;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.3), inset 0 0 8px rgba(16, 185, 129, 0.18) !important;
            backdrop-filter: blur(8px);
        }

        /* Status Badges */
        .status-badge-compact {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            backdrop-filter: blur(8px);
        }
        .badge-ontrack {
            background: rgba(16, 185, 129, 0.14);
            color: #34D399;
            border: 1.5px solid rgba(16, 185, 129, 0.5);
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.35), inset 0 0 6px rgba(16, 185, 129, 0.18);
        }
        .badge-warning {
            background: rgba(245, 158, 11, 0.14);
            color: #FBBF24;
            border: 1.5px solid rgba(245, 158, 11, 0.5);
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.35), inset 0 0 6px rgba(245, 158, 11, 0.18);
        }
        .badge-negative {
            background: rgba(239, 68, 68, 0.14);
            color: #F87171;
            border: 1.5px solid rgba(239, 68, 68, 0.5);
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.35), inset 0 0 6px rgba(239, 68, 68, 0.18);
        }
        .badge-neutral {
            background: rgba(148, 163, 184, 0.14);
            color: #CBD5E1;
            border: 1.5px solid rgba(148, 163, 184, 0.4);
            box-shadow: 0 0 10px rgba(148, 163, 184, 0.2);
        }

        /* Popover Button override */
        div[data-testid="stPopover"] {
            display: inline-flex !important;
            justify-content: flex-end !important;
        }
        div[data-testid="stPopover"] > button {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            font-size: 0.85rem !important;
            color: #64748B !important;
            min-height: unset !important;
            height: 20px !important;
            width: 20px !important;
            box-shadow: none !important;
            line-height: 1 !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stPopover"] > button:hover {
            color: #38BDF8 !important;
            filter: drop-shadow(0 0 6px #38BDF8) !important;
        }

        /* Streamlit Divider & HR */
        hr {
            border: none !important;
            height: 1.5px !important;
            background: linear-gradient(90deg, transparent 5%, rgba(56, 189, 248, 0.5) 30%, rgba(255, 77, 90, 0.5) 70%, transparent 95%) !important;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.35) !important;
            margin: 22px 0 !important;
        }

        /* (Clean deep-space gradient is set in main .stApp block above) */

        /* ========================================================
           ENTRANCE ANIMATIONS
           ======================================================== */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.97); }
            to { opacity: 1; transform: scale(1); }
        }

        div[data-testid="stMetric"],
        div[data-testid="stPlotlyChart"],
        div[data-testid="stDataFrame"],
        div[data-testid="stExpander"] {
            animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        div[data-testid="column"]:nth-child(1) div[data-testid="stMetric"] { animation-delay: 0.04s; }
        div[data-testid="column"]:nth-child(2) div[data-testid="stMetric"] { animation-delay: 0.1s; }
        div[data-testid="column"]:nth-child(3) div[data-testid="stMetric"] { animation-delay: 0.16s; }
        div[data-testid="column"]:nth-child(4) div[data-testid="stMetric"] { animation-delay: 0.22s; }
        div[data-testid="column"]:nth-child(5) div[data-testid="stMetric"] { animation-delay: 0.28s; }

        /* ========================================================
           SHIMMER SWEEP ON HOVER
           ======================================================== */
        @keyframes shimmer-sweep {
            0% { left: -100%; }
            100% { left: 200%; }
        }
        div[data-testid="stMetric"] {
            position: relative !important;
            overflow: hidden !important;
        }
        div[data-testid="stMetric"]::after {
            content: "";
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), rgba(56,189,248,0.06), rgba(255,255,255,0.04), transparent);
            pointer-events: none;
            z-index: 1;
        }
        div[data-testid="stMetric"]:hover::after {
            animation: shimmer-sweep 1s ease-in-out;
        }

        /* ========================================================
           GRADIENT SUBHEADER TEXT
           ======================================================== */
        h3, [data-testid="stSubheader"] {
            background: linear-gradient(135deg, #F8FAFC 0%, #BAE6FD 45%, #C4B5FD 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 700 !important;
        }

        /* ========================================================
           METRIC CARD DELTA ACCENT (LEFT BORDER COLOR)
           ======================================================== */
        div[data-testid="stMetric"]:has([data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Up"]) {
            border-left: 3px solid #10B981 !important;
        }
        div[data-testid="stMetric"]:has([data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Down"]) {
            border-left: 3px solid #EF4444 !important;
        }

        /* ========================================================
           ANIMATED PULSING SECTION DIVIDERS
           ======================================================== */
        @keyframes divider-pulse {
            0%, 100% { box-shadow: 0 0 8px rgba(56, 189, 248, 0.3); opacity: 0.85; }
            50% { box-shadow: 0 0 16px rgba(56, 189, 248, 0.55), 0 0 30px rgba(168, 85, 247, 0.2); opacity: 1; }
        }
        hr { animation: divider-pulse 4s ease-in-out infinite !important; }

        /* ========================================================
           FROSTED GLASS TOOLTIP OVERRIDES
           ======================================================== */
        [data-baseweb="tooltip"] > div {
            background: rgba(10, 16, 28, 0.92) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(56, 189, 248, 0.35) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.75), 0 0 16px rgba(56, 189, 248, 0.2) !important;
            color: #F8FAFC !important;
        }

        /* ========================================================
           SIDEBAR LINK ICON GLOW ON HOVER
           ======================================================== */
        div[data-testid="stSidebar"] a:hover span {
            filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.7)) !important;
        }
        div[data-testid="stSidebar"] a[aria-current="page"] span {
            filter: drop-shadow(0 0 6px rgba(255, 77, 90, 0.7)) !important;
        }

        /* ========================================================
           ANIMATED GRADIENT PROGRESS BARS
           ======================================================== */
        @keyframes progress-gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        div[data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, #38BDF8, #A855F7, #FF4D5A) !important;
            background-size: 200% 100% !important;
            animation: progress-gradient 3s ease infinite !important;
            border-radius: 6px !important;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.5) !important;
        }
        div[data-testid="stProgress"] {
            background: rgba(15, 23, 42, 0.7) !important;
            border-radius: 6px !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
        }

        /* ========================================================
           ENHANCED CHECKBOX & TOGGLE
           ======================================================== */
        div[data-testid="stCheckbox"] label span[data-baseweb="checkbox"] {
            border: 1.5px solid rgba(56, 189, 248, 0.5) !important;
            border-radius: 5px !important;
            background: rgba(10, 16, 28, 0.8) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stCheckbox"] label span[data-baseweb="checkbox"][aria-checked="true"] {
            background: linear-gradient(135deg, #38BDF8, #6366F1) !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.5) !important;
        }

        /* ========================================================
           TEXT-AREA ENHANCEMENTS
           ======================================================== */
        div[data-testid="stTextArea"] textarea {
            background-color: #0A111E !important;
            border: 1.5px solid rgba(56, 189, 248, 0.32) !important;
            color: #F8FAFC !important;
            border-radius: 9px !important;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5), 0 0 8px rgba(56, 189, 248, 0.08) !important;
            font-family: var(--font-main) !important;
            transition: all 0.22s ease !important;
        }
        div[data-testid="stTextArea"] textarea:focus {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3), 0 0 18px rgba(56, 189, 248, 0.4) !important;
        }

        /* ========================================================
           ACCESSIBLE FOCUS RING
           ======================================================== */
        button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible, a:focus-visible {
            outline: 2px solid #38BDF8 !important;
            outline-offset: 2px !important;
            box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.25) !important;
        }

        /* ========================================================
           NOTIFICATION TOAST
           ======================================================== */
        div[data-testid="stToast"] {
            background: rgba(10, 16, 28, 0.95) !important;
            backdrop-filter: blur(16px) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7), 0 0 20px rgba(56, 189, 248, 0.2) !important;
            color: #F8FAFC !important;
        }

        /* ========================================================
           IMAGE & MEDIA BORDERS
           ======================================================== */
        div[data-testid="stImage"] img {
            border: 1.5px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        }

        /* ========================================================
           CAPTION REFINEMENTS
           ======================================================== */
        .stCaption, [data-testid="stCaptionContainer"] {
            color: #64748B !important;
            font-size: 0.76rem !important;
        }

        /* ========================================================
           SPINNER / LOADING ANIMATION OVERRIDE
           ======================================================== */
        div[data-testid="stSpinner"] > div {
            border-color: rgba(56, 189, 248, 0.2) !important;
            border-top-color: #38BDF8 !important;
            filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.5)) !important;
        }

        /* ========================================================
           ENHANCED SECTION HEADER COMPONENT CLASS
           ======================================================== */
        .section-header-enhanced {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 8px 0 18px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        }
        .section-header-enhanced .section-icon {
            font-size: 1.3rem;
            filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.6));
            animation: fadeInScale 0.4s ease both;
        }
        .section-header-enhanced .section-title {
            font-size: 1.15rem;
            font-weight: 800;
            background: linear-gradient(135deg, #F8FAFC 10%, #BAE6FD 50%, #C4B5FD 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        .section-header-enhanced .section-line {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.4), transparent);
        }
        .section-header-enhanced .section-badge {
            font-size: 0.65rem;
            font-weight: 700;
            color: #94A3B8;
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.25);
            padding: 2px 10px;
            border-radius: 12px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        /* ========================================================
           SPARKLINE MINI-CHART CONTAINER
           ======================================================== */
        .sparkline-container {
            display: flex;
            align-items: flex-end;
            gap: 2px;
            height: 28px;
            margin: 8px 0 4px 0;
        }
        .sparkline-bar {
            flex: 1;
            border-radius: 2px 2px 0 0;
            background: linear-gradient(180deg, #38BDF8, rgba(56, 189, 248, 0.3));
            transition: all 0.3s ease;
            min-width: 3px;
        }
        .sparkline-bar:hover {
            background: linear-gradient(180deg, #7DD3FC, rgba(56, 189, 248, 0.5));
            box-shadow: 0 0 6px rgba(56, 189, 248, 0.5);
        }

        /* ========================================================
           DATA PIPELINE STATUS COMPONENT
           ======================================================== */
        .pipeline-status {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 16px;
            background: rgba(10, 16, 28, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 10px;
            margin: 6px 0;
        }
        .pipeline-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .pipeline-dot-active {
            background: #10B981;
            box-shadow: 0 0 8px #10B981, 0 0 16px rgba(16, 185, 129, 0.4);
            animation: pulse-emerald 2s infinite ease-in-out;
        }
        .pipeline-dot-warn {
            background: #F59E0B;
            box-shadow: 0 0 8px #F59E0B;
        }
        .pipeline-dot-error {
            background: #EF4444;
            box-shadow: 0 0 8px #EF4444;
            animation: pulse-red 2s infinite ease-in-out;
        }
        .pipeline-info { flex: 1; }
        .pipeline-name {
            font-size: 0.82rem;
            font-weight: 700;
            color: #F8FAFC;
        }
        .pipeline-detail {
            font-size: 0.7rem;
            color: #64748B;
            margin-top: 1px;
        }
        .pipeline-metric {
            font-size: 0.85rem;
            font-weight: 800;
            color: #38BDF8;
            font-family: var(--font-mono);
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
        }

        </style>
        """.replace("__BG_IMAGE__", _background_image_uri()),
        unsafe_allow_html=True
    )
