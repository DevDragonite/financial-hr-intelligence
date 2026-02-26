# config.py — Dark Earth & Neon Green Executive palette
# Coolors: #2d2d2a · #353831 · #38423b · #3f5e5a · #20fc8f

COLORS = {
    # ── Fondos ──────────────────────────────────────
    "bg_gradient": "linear-gradient(135deg, #2d2d2a 0%, #353831 50%, #2d2d2a 100%)",
    "surface": "rgba(63, 94, 90, 0.15)",
    "surface_hover": "rgba(63, 94, 90, 0.25)",

    # ── Acento principal — Neon Green ───────────────
    "primary": "#20fc8f",
    "primary_soft": "rgba(32, 252, 143, 0.15)",

    # ── Acento secundario — Dark Teal ───────────────
    "secondary": "#3f5e5a",
    "secondary_soft": "rgba(63, 94, 90, 0.18)",

    # ── Surface tones ──────────────────────────────
    "accent": "#38423b",
    "accent_soft": "rgba(56, 66, 59, 0.12)",
    "highlight": "#20fc8f",
    "highlight_soft": "rgba(32, 252, 143, 0.12)",
    "highlight_light": "#20fc8f",

    # ── Semáforo financiero ──────────────────────────
    "positive": "#20fc8f",
    "neutral":  "#8aaa9e",
    "negative": "#e05252",

    # ── Texto ────────────────────────────────────────
    "text_primary": "#e8f4ed",
    "text_muted":   "#8aaa9e",
    "text_accent":  "#20fc8f",

    # ── Bordes ───────────────────────────────────────
    "border":       "rgba(32, 252, 143, 0.15)",
    "border_strong":"rgba(32, 252, 143, 0.35)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font": {
            "family": "Inter, sans-serif",
            "color": "#e8f4ed",
            "size": 12,
        },
        "colorway": [
            "#20fc8f", "#3f5e5a", "#8aaa9e",
            "#5cdb95", "#e05252", "#f0a500",
            "#7b68ee", "#fb923c",
        ],
        "xaxis": {
            "gridcolor": "rgba(32,252,143,0.06)",
            "linecolor": "rgba(32,252,143,0.10)",
            "zerolinecolor": "rgba(32,252,143,0.08)",
        },
        "yaxis": {
            "gridcolor": "rgba(32,252,143,0.06)",
            "linecolor": "rgba(32,252,143,0.10)",
            "zerolinecolor": "rgba(32,252,143,0.08)",
        },
        "legend": {
            "bgcolor":     "rgba(45,45,42,0.8)",
            "bordercolor": "rgba(32,252,143,0.15)",
        },
    }
}
