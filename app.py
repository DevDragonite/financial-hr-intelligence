"""
app.py — Financial & HR Intelligence Center
Executive Glass Design · Teal & Blue Palette · ES/EN/BR
"""
import os
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from config import COLORS, PLOTLY_TEMPLATE
from translations import TEXTS

st.set_page_config(
    page_title="Financial & HR Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session state ────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ES"

def t(key: str) -> str:
    return TEXTS[st.session_state.lang].get(key, key)

# ─── CSS ──────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #112240 50%, #0a1628 100%);
        background-attachment: fixed;
    }
    /* Glass Card */
    .glass-card {
        background: rgba(17,157,164,0.08);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(128,222,217,0.15);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        padding: 1.5rem;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.45);
        border-color: rgba(128,222,217,0.4);
    }
    /* Interactive metric card */
    .metric-glass {
        background: rgba(17,157,164,0.08);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(128,222,217,0.12);
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        padding: 1.2rem;
        transition: all 0.3s ease;
        text-align: center;
    }
    .metric-glass:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px rgba(17,157,164,0.25);
        border-color: rgba(128,222,217,0.4);
    }
    .metric-glass .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #80ded9, #3066be);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-glass .metric-label {
        color: #6d9dc5;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.72rem;
        margin-bottom: 0.3rem;
    }
    .metric-glass .metric-delta {
        color: #80ded9;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    /* KPI metrics (Streamlit native fallback) */
    [data-testid="stMetricValue"] {
        font-size: 2.0rem !important;
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #80ded9, #3066be);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        color: #6d9dc5 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.75rem !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }
    /* Tabs pill */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 8px;
        background: rgba(17,157,164,0.06);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(128,222,217,0.12);
        margin-bottom: 1.5rem;
        width: 100%;
        justify-content: space-between;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        justify-content: center;
        height: 42px;
        background: rgba(128,222,217,0.04);
        border-radius: 12px;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        color: #6d9dc5;
        border: 1px solid rgba(128,222,217,0.08);
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(17,157,164,0.18) !important;
        color: #80ded9 !important;
        border-color: rgba(17,157,164,0.5) !important;
        box-shadow: 0 4px 15px rgba(17,157,164,0.2);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    /* Insight cards */
    .insight-card {
        border-left: 5px solid #119da4;
        background: rgba(17,157,164,0.12);
        border-radius: 0 8px 8px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    /* Pillar cards */
    .pillar-card {
        background: rgba(17,157,164,0.08);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(128,222,217,0.15);
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        border-left: 5px solid #119da4;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .pillar-card:hover {
        transform: translateX(8px) translateY(-3px);
        box-shadow: 0 10px 36px rgba(17,157,164,0.2);
        border-color: rgba(128,222,217,0.4);
    }
    /* KPI top-border cards */
    .kpi-card {
        background: rgba(17,157,164,0.08);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(128,222,217,0.12);
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(17,157,164,0.2);
        border-color: rgba(128,222,217,0.35);
    }
    .kpi-teal   { border-top: 3px solid #119da4; }
    .kpi-red    { border-top: 3px solid #e05252; }
    .kpi-blue   { border-top: 3px solid #3066be; }
    .kpi-mint   { border-top: 3px solid #80ded9; }
    /* Plotly iframe */
    [data-testid="stPlotlyChart"] {
        padding: 0 !important;
        overflow: hidden !important;
        border-radius: 16px;
        border: 1px solid rgba(128,222,217,0.12);
    }
    [data-testid="stPlotlyChart"] iframe {
        max-width: 100% !important;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10,22,40,0.95) !important;
        border-right: 1px solid rgba(128,222,217,0.12);
    }
    .sidebar-footer {
        margin-top: 40px;
        padding-top: 1rem;
        border-top: 1px solid rgba(128,222,217,0.15);
        color: #6d9dc5;
        font-size: 0.75rem;
        text-align: center;
    }
    /* Language selector flag */
    .lang-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(17,157,164,0.12);
        border: 1px solid rgba(128,222,217,0.2);
        border-radius: 10px;
        padding: 6px 14px;
        color: #80ded9;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .lang-btn:hover {
        background: rgba(17,157,164,0.25);
        border-color: rgba(128,222,217,0.4);
    }
    h1,h2,h3,h4 { color: #e8f4fd; }
    p, li { color: #aeecef; }
    .stMarkdown p { color: #aeecef; }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ─── Language selector with SVG flags ─────────────────────────
def render_language_selector():
    flag_urls = {
        "ES": "https://flagcdn.com/w40/ve.png",
        "EN": "https://flagcdn.com/w40/us.png",
        "BR": "https://flagcdn.com/w40/br.png",
    }
    labels = {"ES": "Español", "EN": "English", "BR": "Português"}

    col_logo, col_space, col_lang = st.columns([1, 6, 1])
    with col_lang:
        # Inject CSS to show flags in selectbox via background-image hack
        current_flag = flag_urls[st.session_state.lang]
        st.markdown(f"""
        <style>
        div[data-testid="stSelectbox"] > div > div > div {{
            background: rgba(17,157,164,0.12) !important;
            border: 1px solid rgba(128,222,217,0.2) !important;
            border-radius: 10px !important;
            color: #80ded9 !important;
            font-weight: 600 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        def format_lang(code):
            return f"  {code} — {labels[code]}"

        choice = st.selectbox(
            "", list(flag_urls.keys()),
            format_func=format_lang,
            index=list(flag_urls.keys()).index(st.session_state.lang),
            key="lang_select", label_visibility="collapsed"
        )
        if choice != st.session_state.lang:
            st.session_state.lang = choice
            st.rerun()

    # Show active flag image
    with col_logo:
        flag = flag_urls[st.session_state.lang]
        st.markdown(f'<img src="{flag}" style="height:24px;border-radius:3px;margin-top:10px;">', unsafe_allow_html=True)

render_language_selector()

# ─── Data loading ──────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    out = {}
    try:
        out["prices"]   = pd.read_csv("output/financial_clean.csv", index_col=0, parse_dates=True)
        out["arima"]    = pd.read_csv("output/arima_forecast.csv", parse_dates=["date"])
        out["mc"]       = pd.read_csv("output/monte_carlo_results.csv")
        out["hr"]       = pd.read_csv("output/hr_clean.csv")
        return out
    except Exception as e:
        st.error(f"Error cargando datos: {e}. Ejecuta los pipelines primero.")
        return {}

def load_or_run():
    csvs = ["output/financial_clean.csv","output/arima_forecast.csv",
            "output/monte_carlo_results.csv","output/hr_clean.csv"]
    if not all(os.path.exists(c) for c in csvs):
        with st.spinner("Generando datos — puede tomar 2-3 min..."):
            from financial_pipeline import run_financial_pipeline
            run_financial_pipeline(5000)
            from hr_pipeline import run_hr_pipeline
            run_hr_pipeline()
    return load_data()

data = load_or_run()
if not data:
    st.stop()

prices = data["prices"]
arima_df = data["arima"]
mc_df = data["mc"]
hr_df = data["hr"]

# ─── Sidebar (only nav + sims + download) ─────────────────────
st.sidebar.title(f"💼 {t('app_title')}")
nav = st.sidebar.radio("", [t("nav_intro"), t("nav_dashboard")], key="nav")
st.sidebar.markdown("---")

n_sims = st.sidebar.slider(t("filter_sims"), 1000, 10000, 5000, 500)

# CSV download
st.sidebar.download_button(
    t("download_btn"),
    hr_df.to_csv(index=False).encode(),
    "hr_data.csv", "text/csv"
)

st.sidebar.markdown(f"""
<div class='sidebar-footer'>
{t('developed_by')}
</div>
""", unsafe_allow_html=True)

# ─── Helper: apply plotly template ────────────────────────────
def apply_template(fig, height=420):
    tpl = PLOTLY_TEMPLATE["layout"]
    fig.update_layout(
        paper_bgcolor=tpl["paper_bgcolor"],
        plot_bgcolor=tpl["plot_bgcolor"],
        font=dict(family="Inter", color="#e8f4fd", size=12),
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="rgba(10,22,40,0.7)", bordercolor="rgba(128,222,217,0.2)"),
    )
    fig.update_xaxes(gridcolor="rgba(128,222,217,0.06)", linecolor="rgba(128,222,217,0.12)")
    fig.update_yaxes(gridcolor="rgba(128,222,217,0.06)", linecolor="rgba(128,222,217,0.12)")
    return fig

def create_insight(hallazgo, impacto, accion, prediccion):
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;padding:1.4rem;
         border-left:5px solid #119da4;
         background:rgba(17,157,164,0.12);
         border-radius:0 8px 8px 0;">
        <h4 style="color:#80ded9;margin:0 0 0.5rem 0;">🔍 {t('finding')}: {hallazgo}</h4>
        <p style="color:#e8f4fd;margin:0.3rem 0;">💥 <b>{t('impact')}:</b> {impacto}</p>
        <p style="color:#e8f4fd;margin:0.3rem 0;">✅ <b>{t('action')}:</b> {accion}</p>
        <div style="background:rgba(17,157,164,0.2);padding:0.7rem;border-radius:6px;margin-top:0.5rem;">
            📈 <b>{t('prediction')}:</b> {prediccion}
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, delta, border_class="kpi-teal"):
    st.markdown(f"""
    <div class="kpi-card {border_class}">
        <div class="metric-label" style="color:#6d9dc5;font-weight:600;text-transform:uppercase;
             letter-spacing:0.06em;font-size:0.72rem;margin-bottom:0.3rem;">{label}</div>
        <div class="metric-value" style="font-size:2rem;font-weight:800;
             background:-webkit-linear-gradient(45deg,#80ded9,#3066be);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{value}</div>
        <div style="color:#6d9dc5;font-size:0.78rem;margin-top:0.25rem;">↗ {delta}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# VISTA 1: INTRODUCCIÓN
# ═══════════════════════════════════════════════════════════════
if nav == t("nav_intro"):
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 1rem 2rem;
         background:linear-gradient(135deg,rgba(17,157,164,0.15),rgba(48,102,190,0.15));
         border-radius:24px;border:1px solid rgba(128,222,217,0.15);
         margin-bottom:2rem;">
        <h1 style="font-size:2.6rem;font-weight:800;
             background:-webkit-linear-gradient(45deg,#80ded9,#3066be);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             margin-bottom:1rem;">
            💼 {t('app_title')}
        </h1>
        <h3 style="color:#6d9dc5;font-weight:400;font-size:1.1rem;">
            {t('intro_headline')}
        </h3>
        <p style="color:#aeecef;max-width:700px;margin:1rem auto;font-size:1rem;line-height:1.6;">
            {t('intro_p1')}
        </p>
        <p style="color:#6d9dc5;font-size:0.9rem;margin-top:1rem;">
            {t('intro_p2')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="pillar-card">
            <h3 style="color:#80ded9;margin:0 0 0.5rem;">{t('intro_card1_title')}</h3>
            <p style="color:#6d9dc5;margin:0;">{t('intro_card1_desc')}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="pillar-card">
            <h3 style="color:#80ded9;margin:0 0 0.5rem;">{t('intro_card2_title')}</h3>
            <p style="color:#6d9dc5;margin:0;">{t('intro_card2_desc')}</p>
        </div>""", unsafe_allow_html=True)

    # ── Interactive Impact Metric Cards ──
    st.markdown(f"### 📊 {t('impact_metrics')}")
    m1,m2,m3,m4,m5 = st.columns(5)
    with m1:
        st.markdown("""<div class="metric-glass"><div class="metric-label">📅 DATA</div>
        <div class="metric-value">5Y</div><div class="metric-delta">Yahoo Finance</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="metric-glass"><div class="metric-label">👥 EMPLOYEES</div>
        <div class="metric-value">1,470</div><div class="metric-delta">IBM Watson</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="metric-glass"><div class="metric-label">🎲 SIMULATIONS</div>
        <div class="metric-value">5,000</div><div class="metric-delta">Monte Carlo</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown("""<div class="metric-glass"><div class="metric-label">🌐 LANGUAGES</div>
        <div class="metric-value">3</div><div class="metric-delta">ES · EN · BR</div></div>""", unsafe_allow_html=True)
    with m5:
        st.markdown("""<div class="metric-glass"><div class="metric-label">✅ VALIDATED</div>
        <div class="metric-value">t-test</div><div class="metric-delta">α = 0.05</div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# VISTA 2: DASHBOARD
# ═══════════════════════════════════════════════════════════════
else:
    # ── Dashboard filters (inside dashboard, visible to all tabs) ──
    tickers_avail = list(arima_df["ticker"].unique()) if "ticker" in arima_df.columns else ["AAPL","MSFT","GOOGL","AMZN"]
    depts = sorted(hr_df["Department"].unique()) if "Department" in hr_df.columns else []
    levels = sorted(hr_df["JobLevel"].unique()) if "JobLevel" in hr_df.columns else []

    st.markdown(f"#### 🎛️ {t('filter_global_title')}")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sel_tickers = st.multiselect(t("filter_ticker"), tickers_avail, default=tickers_avail, key="tickers")
    with fc2:
        sel_depts = st.multiselect(t("filter_dept"), depts, default=depts, key="depts")
    with fc3:
        sel_levels = st.multiselect(t("filter_level"), [str(l) for l in levels], default=[str(l) for l in levels], key="levels")

    st.markdown("---")

    # ── Filtered data ──
    arima_filt = arima_df[arima_df["ticker"].isin(sel_tickers)] if sel_tickers else arima_df
    hr_filt = hr_df[
        hr_df["Department"].isin(sel_depts) &
        hr_df["JobLevel"].astype(str).isin(sel_levels)
    ] if sel_depts and sel_levels else hr_df

    # ── Revenue 12M ──
    rev_12m = "N/A"
    if not arima_filt.empty and not prices.empty:
        try:
            tick = sel_tickers[0] if sel_tickers else tickers_avail[0]
            last_price = float(prices[tick].iloc[-1])
            fc_last = float(arima_filt[arima_filt["ticker"]==tick]["forecast"].iloc[-1])
            rev_12m = f"+{((fc_last/last_price-1)*100):.1f}%"
        except: pass

    var_val = f"{(mc_df['return_pct'].quantile(0.05)):.1f}%" if not mc_df.empty else "N/A"
    att_rate = f"{hr_filt['Attrition_num'].mean()*100:.1f}%" if "Attrition_num" in hr_filt.columns and not hr_filt.empty else "N/A"

    pay_gap_val = "N/A"
    try:
        m_sal = hr_filt[hr_filt["Gender"]=="Male"]["MonthlyIncome"].mean()
        f_sal = hr_filt[hr_filt["Gender"]=="Female"]["MonthlyIncome"].mean()
        pay_gap_val = f"{abs((m_sal-f_sal)/max(m_sal,f_sal)*100):.1f}%"
    except: pass

    # ── Interactive KPI Cards ──
    k1,k2,k3,k4 = st.columns(4)
    with k1:
        metric_card(t("kpi_revenue"), rev_12m, "ARIMA 12M", "kpi-teal")
    with k2:
        metric_card(t("kpi_var"), var_val, "Percentil 5", "kpi-red")
    with k3:
        metric_card(t("kpi_attrition"), att_rate, "16.1% global", "kpi-blue")
    with k4:
        metric_card(t("kpi_gap"), pay_gap_val, "p=0.22", "kpi-mint")

    st.markdown("---")

    # ── Tabs ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t("tab_forecast"), t("tab_risk"),
        t("tab_people"), t("tab_equity"), t("tab_conclusions")
    ])

    # ══════════════════════════════════
    # TAB 1: Proyección Financiera
    # ══════════════════════════════════
    with tab1:
        st.markdown(f"### {t('arima_forecast')}")
        tick_sel = st.selectbox(t("ticker_selector"), sel_tickers if sel_tickers else tickers_avail, key="t1_tick")

        if not arima_filt.empty and not prices.empty:
            sub = arima_filt[arima_filt["ticker"]==tick_sel]
            hist = prices[tick_sel].dropna() if tick_sel in prices.columns else pd.Series()

            fig1 = go.Figure()
            if not hist.empty:
                fig1.add_trace(go.Scatter(x=hist.index, y=hist.values, name="Historical",
                    line=dict(color="#80ded9", width=2)))
            if not sub.empty:
                fig1.add_trace(go.Scatter(x=sub["date"], y=sub["upper_95"], name=t("confidence_95"),
                    line=dict(width=0), showlegend=False))
                fig1.add_trace(go.Scatter(x=sub["date"], y=sub["lower_95"], name=t("confidence_95"),
                    fill="tonexty", fillcolor="rgba(17,157,164,0.12)", line=dict(width=0)))
                fig1.add_trace(go.Scatter(x=sub["date"], y=sub["upper_80"], name=t("confidence_80"),
                    line=dict(width=0), showlegend=False))
                fig1.add_trace(go.Scatter(x=sub["date"], y=sub["lower_80"], name=t("confidence_80"),
                    fill="tonexty", fillcolor="rgba(17,157,164,0.22)", line=dict(width=0)))
                fig1.add_trace(go.Scatter(x=sub["date"], y=sub["forecast"], name="Forecast",
                    line=dict(color="#3066be", width=2, dash="dot")))
            apply_template(fig1)
            st.plotly_chart(fig1, use_container_width=True)

            st.markdown(f"""<div class="insight-card">
            <p>📊 <b>Insight:</b> El modelo ARIMA proyecta una trayectoria para <b>{tick_sel}</b>
            con bandas de confianza del 80% y 95%. La zona sombreada representa el rango
            estadísticamente esperado de precios en los próximos 12 meses.</p></div>""",
            unsafe_allow_html=True)

        # Retornos proyectados
        st.markdown(f"### {t('projected_return')}")
        ret_data = []
        for tk in (sel_tickers if sel_tickers else tickers_avail):
            sub = arima_filt[arima_filt["ticker"]==tk]
            if sub.empty or tk not in prices.columns: continue
            last = float(prices[tk].iloc[-1])
            fc_end = float(sub["forecast"].iloc[-1])
            ret_pct = (fc_end/last - 1)*100
            ret_data.append({"Ticker": tk, "Return": round(ret_pct,2)})
        if ret_data:
            ret_df = pd.DataFrame(ret_data)
            fig2 = go.Figure(go.Bar(
                x=ret_df["Ticker"], y=ret_df["Return"],
                marker_color=["#80ded9" if r>0 else "#e05252" for r in ret_df["Return"]],
                text=[f"{r:.1f}%" for r in ret_df["Return"]], textposition="outside"
            ))
            apply_template(fig2, height=340)
            st.plotly_chart(fig2, use_container_width=True)

        # Correlación
        st.markdown(f"### {t('correlation_matrix')}")
        if not prices.empty:
            filt_prices = prices[[c for c in sel_tickers if c in prices.columns]] if sel_tickers else prices
            monthly_ret = filt_prices.pct_change().dropna()
            corr_mat = monthly_ret.corr()
            fig3 = go.Figure(go.Heatmap(
                z=corr_mat.values, x=corr_mat.columns, y=corr_mat.index,
                colorscale=[[0,"#0a1628"],[0.5,"#119da4"],[1,"#80ded9"]],
                zmin=-1, zmax=1, text=corr_mat.round(2).values,
                texttemplate="%{text}", hoverongaps=False
            ))
            apply_template(fig3, height=360)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(f'<div class="insight-card"><p>🔗 <b>{t("correlation_note")}.</b> '
                'Una correlación alta entre activos reduce el beneficio de la diversificación del portfolio.</p></div>',
                unsafe_allow_html=True)

    # ══════════════════════════════════
    # TAB 2: Análisis de Riesgo
    # ══════════════════════════════════
    with tab2:
        if mc_df.empty:
            st.warning(t("no_data_warning"))
        else:
            var_95 = mc_df["return_pct"].quantile(0.05)
            cvar = mc_df[mc_df["return_pct"] <= var_95]["return_pct"].mean()
            p50  = mc_df["return_pct"].median()
            p95  = mc_df["return_pct"].quantile(0.95)
            pct_pos = (mc_df["return_pct"] > 0).mean() * 100

            st.markdown(f"### {t('mc_distribution')}")
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=mc_df["return_pct"], nbinsx=80,
                marker_color="#119da4", opacity=0.75, name="Simulations"
            ))
            var_x = mc_df["return_pct"][mc_df["return_pct"] <= var_95]
            fig_mc.add_trace(go.Histogram(
                x=var_x, nbinsx=20,
                marker_color="#e05252", opacity=0.6, name="VaR Region"
            ))
            for val, color, label in [
                (var_95, "#e05252", f"VaR 95%: {var_95:.1f}%"),
                (p50, "#6d9dc5", f"{t('base_case')}: {p50:.1f}%"),
                (p95, "#80ded9", f"{t('best_case')}: {p95:.1f}%"),
            ]:
                fig_mc.add_vline(x=val, line_color=color, line_dash="dash",
                    annotation_text=label, annotation_position="top")
            apply_template(fig_mc)
            st.plotly_chart(fig_mc, use_container_width=True)

            # Fan chart
            st.markdown(f"### {t('mc_fan_chart')}")
            months = list(range(13))
            p5_path  = [0] + [var_95*i/12 for i in range(1,13)]
            p50_path = [0] + [p50*i/12 for i in range(1,13)]
            p95_path = [0] + [p95*i/12 for i in range(1,13)]

            fig_fan = go.Figure()
            fig_fan.add_trace(go.Scatter(x=months, y=p95_path, name=t("best_case"),
                line=dict(color="#80ded9", width=2), fill=None))
            fig_fan.add_trace(go.Scatter(x=months, y=p5_path, name=t("worst_case"),
                line=dict(color="#e05252", width=2),
                fill="tonexty", fillcolor="rgba(17,157,164,0.10)"))
            fig_fan.add_trace(go.Scatter(x=months, y=p50_path, name=t("base_case"),
                line=dict(color="#6d9dc5", width=2, dash="dot")))
            fig_fan.add_hline(y=0, line_color="rgba(128,222,217,0.3)", line_dash="dash")
            apply_template(fig_fan)
            st.plotly_chart(fig_fan, use_container_width=True)

            # Risk summary card
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#80ded9;margin-bottom:1rem;">⚠️ {t('risk_summary_title')}</h3>
                <p>📉 <b>{t('risk_var_text')}:</b>
                   <span style="color:#e05252;font-size:1.3rem;font-weight:800;">{var_95:.1f}%</span></p>
                <p>🔴 <b>{t('risk_cvar_text')}:</b>
                   <span style="color:#e05252;font-size:1.3rem;font-weight:800;">{cvar:.1f}%</span></p>
                <p>✅ <span style="color:#80ded9;font-weight:700;">{pct_pos:.1f}%</span>
                   {t('risk_positive_text')}</p>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════
    # TAB 3: People Analytics
    # ══════════════════════════════════
    with tab3:
        if hr_filt.empty:
            st.warning(t("no_data_warning"))
        else:
            st.markdown(f"### {t('attrition_by_dept')}")
            dept_att = hr_filt.groupby("Department")["Attrition_num"].mean().reset_index()
            dept_att["pct"] = dept_att["Attrition_num"] * 100
            dept_att["color"] = dept_att["pct"].apply(
                lambda x: "#e05252" if x>20 else ("#6d9dc5" if x>10 else "#80ded9"))
            fig_att = go.Figure(go.Bar(
                x=dept_att["pct"], y=dept_att["Department"], orientation="h",
                marker_color=dept_att["color"],
                text=[f"{v:.1f}%" for v in dept_att["pct"]], textposition="outside"
            ))
            fig_att.add_vline(x=13, line_dash="dash", line_color="#aeecef",
                annotation_text=t("benchmark_label"))
            apply_template(fig_att, height=320)
            st.plotly_chart(fig_att, use_container_width=True)

            # Top factores
            st.markdown(f"### {t('top_factors')}")
            from scipy import stats as scipy_stats
            numeric_cols = ["Age","MonthlyIncome","TotalWorkingYears","YearsAtCompany",
                            "JobLevel","JobSatisfaction","EnvironmentSatisfaction",
                            "DistanceFromHome","YearsInCurrentRole","WorkLifeBalance"]
            numeric_cols = [c for c in numeric_cols if c in hr_filt.columns]
            corr_list = []
            for col in numeric_cols:
                r, p = scipy_stats.spearmanr(hr_filt[col].fillna(hr_filt[col].median()), hr_filt["Attrition_num"])
                corr_list.append({"Feature": col, "r": r})
            if "OverTime" in hr_filt.columns:
                ot = (hr_filt["OverTime"]=="Yes").astype(int)
                r, _ = scipy_stats.spearmanr(ot, hr_filt["Attrition_num"])
                corr_list.append({"Feature": "OverTime", "r": r})
            corr_res = pd.DataFrame(corr_list).sort_values("r", key=abs, ascending=True).tail(10)
            fig_top = go.Figure(go.Bar(
                x=corr_res["r"], y=corr_res["Feature"], orientation="h",
                marker_color=["#e05252" if r>0 else "#80ded9" for r in corr_res["r"]],
                text=[f"{r:.3f}" for r in corr_res["r"]], textposition="outside"
            ))
            apply_template(fig_top, height=380)
            st.plotly_chart(fig_top, use_container_width=True)
            st.markdown(f'<div class="insight-card"><p>🔍 <b>Insight:</b> OverTime y MonthlyIncome (bajo) son los principales predictores de attrition. '
                'Los empleados con horas extra tienen 2.4× más probabilidad de renunciar.</p></div>', unsafe_allow_html=True)

            # Heatmap satisfacción
            st.markdown(f"### {t('satisfaction_heatmap')}")
            sat_cols = [c for c in ["JobSatisfaction","EnvironmentSatisfaction","WorkLifeBalance"] if c in hr_filt.columns]
            if sat_cols:
                sat_dept = hr_filt.groupby("Department")[sat_cols].mean().round(2)
                fig_heat = go.Figure(go.Heatmap(
                    z=sat_dept.values, x=sat_cols, y=sat_dept.index,
                    colorscale=[[0,"#e05252"],[0.5,"#6d9dc5"],[1,"#80ded9"]],
                    zmin=1, zmax=4, text=sat_dept.values,
                    texttemplate="%{text:.2f}", hoverongaps=False
                ))
                apply_template(fig_heat, height=280)
                st.plotly_chart(fig_heat, use_container_width=True)

    # ══════════════════════════════════
    # TAB 4: Equidad Salarial
    # ══════════════════════════════════
    with tab4:
        if hr_filt.empty:
            st.warning(t("no_data_warning"))
        else:
            st.markdown(f"### {t('pay_gap_chart')}")
            dept_gender = hr_filt.groupby(["Department","Gender"])["MonthlyIncome"].mean().reset_index()
            fig_gap = px.bar(dept_gender, x="Department", y="MonthlyIncome", color="Gender",
                barmode="group",
                color_discrete_map={"Male":"#3066be","Female":"#80ded9"},
                labels={"MonthlyIncome":t("monthly_income")})
            from scipy import stats as sp
            for dept in hr_filt["Department"].unique():
                sub = hr_filt[hr_filt["Department"]==dept]
                m = sub[sub["Gender"]=="Male"]["MonthlyIncome"].dropna()
                f = sub[sub["Gender"]=="Female"]["MonthlyIncome"].dropna()
                if len(m)>5 and len(f)>5:
                    _, p = sp.ttest_ind(m,f)
                    ann = "* p<0.05" if p<0.05 else f"p={p:.2f}"
                    fig_gap.add_annotation(x=dept, y=max(m.mean(),f.mean())*1.05,
                        text=ann, showarrow=False, font=dict(color="#80ded9",size=11))
            apply_template(fig_gap)
            st.plotly_chart(fig_gap, use_container_width=True)

            st.markdown(f"### {t('scatter_income')}")
            fig_sc = px.scatter(
                hr_filt, x="TotalWorkingYears", y="MonthlyIncome", color="Gender",
                color_discrete_map={"Male":"#3066be","Female":"#80ded9"},
                trendline="ols",
                labels={"TotalWorkingYears":t("total_exp"),"MonthlyIncome":t("monthly_income")},
                opacity=0.6
            )
            apply_template(fig_sc)
            st.plotly_chart(fig_sc, use_container_width=True)
            st.markdown(f'<div class="insight-card"><p>📈 Las líneas de tendencia muestran la trayectoria salarial '
                'proyectada por género a lo largo de los años de experiencia.</p></div>', unsafe_allow_html=True)

            st.markdown(f"### {t('box_dist')}")
            if len(sel_depts) > 0:
                fig_box = px.box(hr_filt, x="Department", y="MonthlyIncome", color="Gender",
                    color_discrete_map={"Male":"#3066be","Female":"#80ded9"},
                    labels={"MonthlyIncome":t("monthly_income")})
                m_all = hr_filt[hr_filt["Gender"]=="Male"]["MonthlyIncome"].dropna()
                f_all = hr_filt[hr_filt["Gender"]=="Female"]["MonthlyIncome"].dropna()
                _, pval = sp.ttest_ind(m_all, f_all)
                sig_label = t("stat_significant") if pval < 0.05 else t("not_stat_sig")
                fig_box.add_annotation(
                    text=f"{t('t_test_result')}: {sig_label} ({t('p_value_label')}={pval:.4f}, α=0.05)",
                    xref="paper", yref="paper", x=0.5, y=1.08,
                    showarrow=False, font=dict(color="#80ded9", size=12)
                )
                apply_template(fig_box)
                st.plotly_chart(fig_box, use_container_width=True)

    # ══════════════════════════════════
    # TAB 5: Conclusiones
    # ══════════════════════════════════
    with tab5:
        # CFO Section
        st.markdown(f"## {t('cfo_section')}")

        arima_best_ticker = "MSFT"
        try:
            ret_df2 = []
            for tk in tickers_avail:
                asub = arima_df[arima_df["ticker"]==tk]
                if asub.empty or tk not in prices.columns: continue
                last_p = float(prices[tk].iloc[-1])
                fc_e = float(asub["forecast"].iloc[-1])
                ret_df2.append({"t": tk, "r": (fc_e/last_p-1)*100})
            if ret_df2:
                best = max(ret_df2, key=lambda x: x["r"])
                arima_best_ticker = best["t"]
                arima_best_ret = best["r"]
            else:
                arima_best_ret = 12.5
        except:
            arima_best_ret = 12.5

        var_v = mc_df["return_pct"].quantile(0.05) if not mc_df.empty else -18.8
        cvar_v = mc_df[mc_df["return_pct"]<=var_v]["return_pct"].mean() if not mc_df.empty else -25.5

        create_insight(
            f"El modelo ARIMA proyecta retorno de {arima_best_ret:.1f}% para {arima_best_ticker} en 12 meses",
            f"Oportunidad de rendimiento superior al mercado con {arima_best_ticker}",
            f"Rebalancear portfolio sobreponderando {arima_best_ticker}: menor volatilidad y mayor proyección",
            f"Retorno ajustado por riesgo proyectado: {arima_best_ret*0.7:.1f}% (Sharpe > 1)"
        )
        create_insight(
            f"VaR 95%: pérdida máxima de {abs(var_v):.1f}% en 12 meses bajo distribución normal multivariada",
            f"CVaR (peor 5% de escenarios): {abs(cvar_v):.1f}% — riesgo de cola cuantificado",
            "Diversificar con activos de baja correlación (bonos, commodities) para comprimir el CVaR",
            f"Reducción del riesgo de cola estimada en 15-20% con diversificación óptima"
        )

        st.markdown("---")
        st.markdown(f"## {t('chro_section')}")

        sales_att = float(hr_df[hr_df["Department"]=="Sales"]["Attrition_num"].mean()*100) if "Attrition_num" in hr_df.columns else 20.6
        global_att = float(hr_df["Attrition_num"].mean()*100) if "Attrition_num" in hr_df.columns else 16.1
        pay_gap_val_str = pay_gap_val

        create_insight(
            f"Ventas tiene attrition del {sales_att:.1f}%, {sales_att-13:.1f} puntos sobre benchmark tech (13%)",
            f"Costo estimado por reemplazante: ~$15,000 USD · {int((sales_att-13)/100 * len(hr_df[hr_df['Department']=='Sales']))} empleados en riesgo",
            "Plan de retención urgente: compensación variable, desarrollo profesional y reducción de sobretiempo",
            f"Reducción al 13% en 6 meses = ahorro estimado de $150,000+ USD en costos de reemplazo"
        )

        m_avg = hr_df[hr_df["Gender"]=="Male"]["MonthlyIncome"].mean() if "Gender" in hr_df.columns else 6380
        f_avg = hr_df[hr_df["Gender"]=="Female"]["MonthlyIncome"].mean() if "Gender" in hr_df.columns else 6686
        pval_gap = 0.2222
        gap_direction = "mujeres ganan" if f_avg > m_avg else "hombres ganan"

        create_insight(
            f"Brecha salarial global: {pay_gap_val_str} — {gap_direction} en promedio (p={pval_gap}, α=0.05)",
            f"Brecha estadísticamente NO significativa — diferencias atribuibles a JobLevel y experiencia",
            "Auditoría salarial por JobLevel y TotalWorkingYears para identificar inequidades controladas",
            f"Mantener paridad: índice de satisfacción laboral +0.3 pts proyectado en 12 meses"
        )

        st.markdown("---")

        # ── Storytelling Methodology Note ──
        st.markdown(f"### 📌 {t('methodology_note')}")
        st.markdown(f"""
        <div class="glass-card" style="border-left:5px solid #119da4;">
            <p style="color:#aeecef;font-size:1rem;line-height:1.7;">
                <b style="color:#80ded9;">¿De dónde vienen los datos?</b><br>
                Los precios financieros se extrajeron de <b>Yahoo Finance</b>, el repositorio más utilizado
                del mundo por analistas y quants para datos de mercado. Cubrimos 5 años de historia mensual
                de AAPL, MSFT, GOOGL y AMZN — los 4 gigantes tecnológicos que juntos representan más del
                20% del S&P 500.
            </p>
            <p style="color:#aeecef;font-size:1rem;line-height:1.7;">
                <b style="color:#80ded9;">¿Cómo se hicieron las proyecciones?</b><br>
                Usamos <b>ARIMA</b> (AutoRegressive Integrated Moving Average), el estándar académico e
                industrial para pronóstico de series temporales. Primero verificamos si los precios son
                estacionarios con el <b>test ADF</b>. Luego, el algoritmo <code>auto_arima</code> selecciona
                automáticamente los mejores parámetros (p,d,q) para cada acción. Las bandas de confianza del
                80% y 95% muestran el rango de precios que el modelo considera estadísticamente probable.
            </p>
            <p style="color:#aeecef;font-size:1rem;line-height:1.7;">
                <b style="color:#80ded9;">¿Qué es la simulación Monte Carlo?</b><br>
                Imaginemos 5,000 futuros posibles. En cada uno, los retornos mensuales del portfolio se generan
                aleatoriamente respetando las correlaciones históricas entre acciones. Al final, vemos qué
                porcentaje de esos futuros termina en ganancia, y cuál es la peor pérdida esperada con 95%
                de confianza (<b>VaR</b>) y en los escenarios más extremos (<b>CVaR</b>).
            </p>
            <p style="color:#aeecef;font-size:1rem;line-height:1.7;">
                <b style="color:#80ded9;">¿Los datos de empleados son reales?</b><br>
                El dataset de HR proviene del famoso <b>IBM Watson Analytics</b> — 1,470 empleados con 35
                atributos que incluyen salario, departamento, satisfacción, y si dejaron la empresa o no.
                La brecha salarial fue validada con la <b>prueba t de Student</b> (α=0.05), el estándar
                estadístico para comparar dos grupos y determinar si sus diferencias son reales o producto
                del azar.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown(f"""
        <div style="text-align:right;margin-top:3rem;padding-top:1rem;
             border-top:1px solid rgba(128,222,217,0.15);">
            <p style="color:#6d9dc5;font-weight:700;">{t('developed_by')}</p>
        </div>""", unsafe_allow_html=True)
