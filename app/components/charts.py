import plotly.graph_objects as go

# Enterprise Luxury Dark Cyber Palette
ENTERPRISE_COLOR_PALETTE = [
    "#38BDF8",  # Cyber Cyan
    "#FF4D5A",  # Crimson Neon
    "#10B981",  # Emerald Green
    "#A855F7",  # Royal Violet
    "#F59E0B",  # Amber Gold
    "#818CF8",  # Tech Indigo
    "#EC4899",  # Electric Pink
    "#06B6D4",  # Turquoise
    "#F97316",  # Vibrant Orange
]

def apply_chart_theme(fig, title: str = "", height: int = 340):
    """
    Applies unified enterprise dark luxury theme with seamless transparency & contrast:
    - Background: Transparent rgba(0,0,0,0) (seamlessly absorbs card gradient)
    - Gridlines: rgba(56, 189, 248, 0.08) for subtle ethereal grid
    - Typography: Plus Jakarta Sans with crisp antialiased rendering
    - Hover labels: Glassmorphic obsidian container with glowing cyan rim
    - Pie / Donut charts: Dark separator lines, elegant percentages, and centered donut metrics
    """
    fig.update_layout(
        title={
            "text": title if title else (fig.layout.title.text if fig.layout.title else ""),
            "font": {
                "size": 13,
                "color": "#F8FAFC",
                "family": "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"
            },
            "x": 0.02,
            "xanchor": "left"
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=45, b=25),
        height=height,
        font=dict(
            color="#94A3B8",
            family="'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            size=11
        ),
        hoverlabel=dict(
            bgcolor="rgba(10, 16, 28, 0.95)",
            font_size=12,
            font_family="'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            font_color="#F8FAFC",
            bordercolor="#38BDF8"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#94A3B8")
        )
    )

    # For Cartesian charts
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(56, 189, 248, 0.08)",
        gridwidth=1,
        zeroline=False,
        linecolor="rgba(56, 189, 248, 0.2)",
        tickfont=dict(color="#94A3B8", size=11)
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(56, 189, 248, 0.08)",
        gridwidth=1,
        zeroline=False,
        linecolor="rgba(56, 189, 248, 0.2)",
        tickfont=dict(color="#94A3B8", size=11)
    )

    # For Pie / Donut charts
    for trace in fig.data:
        if trace.type == "pie":
            trace.update(
                textfont=dict(
                    color="#FFFFFF",
                    size=12,
                    family="'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"
                ),
                marker=dict(line=dict(color="#060911", width=2.5))
            )

    return fig


def apply_geo_map_theme(fig, title: str = "", height: int = 540):
    """
    Applies unified enterprise dark luxury theme for choropleth and geographic maps:
    - Deep obsidian ocean & lake background
    - High-contrast country outlines in glowing cyber cyan
    - Antialiased typography and glassmorphic hovercards
    """
    apply_chart_theme(fig, title=title, height=height)
    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(56, 189, 248, 0.35)",
        coastlinewidth=1,
        showocean=True,
        oceancolor="rgba(6, 11, 21, 0.95)",
        showlakes=True,
        lakecolor="rgba(8, 14, 26, 0.95)",
        showland=True,
        landcolor="rgba(15, 23, 42, 0.75)",
        showcountries=True,
        countrycolor="rgba(56, 189, 248, 0.25)",
        countrywidth=0.8,
        bgcolor="rgba(0, 0, 0, 0)"
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=10),
        coloraxis_colorbar=dict(
            title=dict(font=dict(color="#94A3B8", size=11)),
            tickfont=dict(color="#94A3B8", size=10),
            thickness=14,
            len=0.75,
            x=0.98,
            bgcolor="rgba(10, 16, 28, 0.6)",
            outlinecolor="rgba(56, 189, 248, 0.2)",
            outlinewidth=1
        )
    )
    return fig

