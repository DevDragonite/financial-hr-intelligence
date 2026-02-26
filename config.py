# config.py — Deep Navy Executive Glass palette
# Coolors: #b9d6f2 · #061a40 · #0353a4 · #006daa · #003559

COLORS = {
    # ── Fondos ──────────────────────────────────────
    "bg_gradient": "linear-gradient(135deg, #061a40 0%, #003559 50%, #061a40 100%)",
    "surface": "rgba(3, 83, 164, 0.12)",
    "surface_hover": "rgba(3, 83, 164, 0.22)",

    # ── Acento principal — Azul royal ───────────────
    "primary": "#0353a4",
    "primary_soft": "rgba(3, 83, 164, 0.18)",

    # ── Acento secundario — Cerulean ────────────────
    "secondary": "#006daa",
    "secondary_soft": "rgba(0, 109, 170, 0.18)",

    # ── Acento terciario — Lt Blue highlight ────────
    "accent": "#b9d6f2",
    "accent_soft": "rgba(185, 214, 242, 0.12)",

    # ── Semáforo financiero ──────────────────────────
    "positive": "#4caf82",     # Verde institucional
    "neutral":  "#f0a500",     # Ámbar
    "negative": "#e05252",     # Rojo suave

    # ── Texto ────────────────────────────────────────
    "text_primary": "#e8f4fd",
    "text_muted":   "#7ba7c9",
    "text_accent":  "#b9d6f2",

    # ── Bordes ───────────────────────────────────────
    "border":       "rgba(185, 214, 242, 0.20)",
    "border_strong":"rgba(185, 214, 242, 0.45)",
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
            "#b9d6f2", "#0353a4", "#006daa",
            "#4caf82", "#f0a500", "#e05252",
            "#7b68ee", "#fb923c",
        ],
        "xaxis": {
            "gridcolor": "rgba(185,214,242,0.06)",
            "linecolor": "rgba(185,214,242,0.12)",
            "zerolinecolor": "rgba(185,214,242,0.10)",
        },
        "yaxis": {
            "gridcolor": "rgba(185,214,242,0.06)",
            "linecolor": "rgba(185,214,242,0.12)",
            "zerolinecolor": "rgba(185,214,242,0.10)",
        },
        "legend": {
            "bgcolor":     "rgba(6,26,64,0.7)",
            "bordercolor": "rgba(185,214,242,0.20)",
        },
    }
}
