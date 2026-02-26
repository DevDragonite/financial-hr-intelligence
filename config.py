# config.py — Teal & Blue Executive Glass palette
# Coolors: #3066be · #119da4 · #6d9dc5 · #80ded9 · #aeecef

COLORS = {
    # ── Fondos ──────────────────────────────────────
    "bg_gradient": "linear-gradient(135deg, #0a1628 0%, #112240 50%, #0a1628 100%)",
    "surface": "rgba(17, 157, 164, 0.10)",
    "surface_hover": "rgba(17, 157, 164, 0.18)",

    # ── Acento principal — Royal Blue ───────────────
    "primary": "#3066be",
    "primary_soft": "rgba(48, 102, 190, 0.18)",

    # ── Acento secundario — Teal ────────────────────
    "secondary": "#119da4",
    "secondary_soft": "rgba(17, 157, 164, 0.18)",

    # ── Acento terciario — Steel Blue ───────────────
    "accent": "#6d9dc5",
    "accent_soft": "rgba(109, 157, 197, 0.12)",

    # ── Highlight — Aqua / Mint ─────────────────────
    "highlight": "#80ded9",
    "highlight_soft": "rgba(128, 222, 217, 0.12)",
    "highlight_light": "#aeecef",

    # ── Semáforo financiero ──────────────────────────
    "positive": "#80ded9",
    "neutral":  "#6d9dc5",
    "negative": "#e05252",

    # ── Texto ────────────────────────────────────────
    "text_primary": "#e8f4fd",
    "text_muted":   "#6d9dc5",
    "text_accent":  "#80ded9",

    # ── Bordes ───────────────────────────────────────
    "border":       "rgba(128, 222, 217, 0.18)",
    "border_strong":"rgba(128, 222, 217, 0.40)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font": {
            "family": "Inter, sans-serif",
            "color": "#e8f4fd",
            "size": 12,
        },
        "colorway": [
            "#80ded9", "#3066be", "#119da4",
            "#6d9dc5", "#aeecef", "#e05252",
            "#7b68ee", "#fb923c",
        ],
        "xaxis": {
            "gridcolor": "rgba(128,222,217,0.06)",
            "linecolor": "rgba(128,222,217,0.12)",
            "zerolinecolor": "rgba(128,222,217,0.10)",
        },
        "yaxis": {
            "gridcolor": "rgba(128,222,217,0.06)",
            "linecolor": "rgba(128,222,217,0.12)",
            "zerolinecolor": "rgba(128,222,217,0.10)",
        },
        "legend": {
            "bgcolor":     "rgba(10,22,40,0.7)",
            "bordercolor": "rgba(128,222,217,0.20)",
        },
    }
}
