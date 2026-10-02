def render_status_badge(status: str) -> str:
    """
    Renders compact enterprise status badge with illuminated neon outlines and ambient glowing light:
    ● ON TRACK
    ● ABOVE TARGET
    ● BELOW TARGET
    ● WARNING
    ● INSUFFICIENT DATA
    """
    s = status.upper().strip()
    if "ON TRACK" in s or "PASS" in s or "POSITIVE" in s or "MET" in s or "FRESH" in s or "CONNECTED" in s:
        color = "#34D399"
        bg = "rgba(16, 185, 129, 0.14)"
        border = "rgba(16, 185, 129, 0.45)"
        glow = "rgba(16, 185, 129, 0.35)"
    elif "WARNING" in s or "REVIEW" in s or "NEAR" in s or "UNDERSPENDING" in s or "BREAK-EVEN" in s:
        color = "#FBBF24"
        bg = "rgba(245, 158, 11, 0.14)"
        border = "rgba(245, 158, 11, 0.45)"
        glow = "rgba(245, 158, 11, 0.35)"
    elif "BELOW" in s or "OVERSPENDING" in s or "NEGATIVE" in s or "FAILED" in s:
        color = "#F87171"
        bg = "rgba(239, 68, 68, 0.14)"
        border = "rgba(239, 68, 68, 0.45)"
        glow = "rgba(239, 68, 68, 0.35)"
    else:
        color = "#CBD5E1"
        bg = "rgba(148, 163, 184, 0.14)"
        border = "rgba(148, 163, 184, 0.35)"
        glow = "rgba(148, 163, 184, 0.2)"

    return (
        f'<span style="display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; '
        f'border-radius: 20px; font-size: 0.72rem; font-weight: 700; background: {bg}; color: {color}; '
        f'border: 1px solid {border}; box-shadow: 0 0 10px {glow}, inset 0 0 6px {glow}; '
        f'letter-spacing: 0.04em; text-transform: uppercase; backdrop-filter: blur(6px);">'
        f'<span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: {color}; box-shadow: 0 0 8px {color};"></span>'
        f'{status}</span>'
    )
