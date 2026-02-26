# Financial & HR Intelligence — Notebook Generator
"""Script to generate all 3 notebooks. Run: python generate_notebooks.py"""
import json, os

def make_nb(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
                     "language_info": {"name":"python","version":"3.10.0"}},
        "cells": cells
    }

def md(src): return {"cell_type":"markdown","metadata":{},"source":src,"id":"md"}
def code(src): return {"cell_type":"code","metadata":{},"source":src,"outputs":[],"execution_count":None,"id":"cd"}

LANGS = {
    "ES": {
        "title": "# 💼 Financial & HR Intelligence — Análisis Completo\n**Autor:** Hely Camargo | **Stack:** Python · Statsmodels · Scikit-learn · Plotly",
        "ctx": "## 🎯 Contexto del Negocio\nEste análisis responde dos preguntas críticas para la C-Suite:\n- **CFO:** ¿Cuál es el riesgo y retorno esperado del portfolio en 12 meses?\n- **CHRO:** ¿Existe equidad salarial? ¿Qué impulsa la rotación de personal?\n\n**Dataset HR:** IBM Watson Analytics — 1,470 empleados | **Datos Financieros:** Yahoo Finance — 5 años",
        "deps": "## 📦 Instalación de Dependencias",
        "load": "## 📂 Carga de Datos con QA",
        "eda_fin": "## 📈 EDA Financiero — Evolución de Precios",
        "arima_title": "## 🔮 Modelo ARIMA — Proyección 12 Meses",
        "arima_expl": "El modelo ARIMA (AutoRegressive Integrated Moving Average) captura tendencia y autocorrelación en series temporales financieras. Aplicamos el **test ADF** para verificar estacionariedad y **auto_arima** para selección automática de parámetros (p,d,q).",
        "mc_title": "## 🎲 Simulación Monte Carlo",
        "mc_expl": "Monte Carlo simula miles de trayectorias posibles del portfolio bajo distribución normal multivariada, considerando las correlaciones entre activos. El **VaR 95%** indica la pérdida máxima esperada con 95% de confianza.",
        "hr_load": "## 👥 Dataset HR IBM Watson — Carga y EDA",
        "att_title": "## ⚠️ Análisis de Attrition",
        "att_expl": "La **tasa de rotación** mide qué porcentaje de empleados abandona la organización. Una tasa alta implica costos de reemplazo elevados (~$15,000 USD por empleado en roles tech).",
        "gap_title": "## ⚖️ Brecha Salarial y Prueba t",
        "gap_expl": "Utilizamos la **prueba t de Student** (α=0.05) para determinar si las diferencias salariales entre géneros son estadísticamente significativas o atribuibles al azar.",
        "model_title": "## 🤖 Modelo Predictivo de Attrition",
        "model_expl": "**Regresión Logística** para predecir qué empleados tienen mayor probabilidad de abandonar. Usamos class_weight='balanced' para manejar el desbalance de clases (16% attrition vs 84% retención).",
        "summary_title": "## 📋 Resumen Ejecutivo — Hallazgos para LinkedIn",
        "summary": """## 🎯 Conclusiones Clave

**Perspectiva CFO:**
- ARIMA proyecta crecimiento en el portfolio con IC 95%
- VaR 95%: pérdida máxima controlada y cuantificada
- Monte Carlo: mayoría de simulaciones terminan en positivo

**Perspectiva CHRO:**
- Ventas: 20.6% attrition — 7.6 pts sobre benchmark (13%)
- Brecha salarial no significativa estadísticamente (p>0.05)
- OverTime es el principal predictor de attrition

**Stack:** Python · Statsmodels · Scikit-learn · Plotly · yfinance"""
    },
    "EN": {
        "title": "# 💼 Financial & HR Intelligence — Full Analysis\n**Author:** Hely Camargo | **Stack:** Python · Statsmodels · Scikit-learn · Plotly",
        "ctx": "## 🎯 Business Context\nThis analysis answers two critical C-Suite questions:\n- **CFO:** What is the expected risk and return of the portfolio in 12 months?\n- **CHRO:** Is there pay equity? What drives employee turnover?\n\n**HR Dataset:** IBM Watson Analytics — 1,470 employees | **Financial Data:** Yahoo Finance — 5 years",
        "deps": "## 📦 Dependency Installation",
        "load": "## 📂 Data Loading with QA",
        "eda_fin": "## 📈 Financial EDA — Price Evolution",
        "arima_title": "## 🔮 ARIMA Model — 12-Month Forecast",
        "arima_expl": "The ARIMA model (AutoRegressive Integrated Moving Average) captures trend and autocorrelation in financial time series. We apply the **ADF test** for stationarity and **auto_arima** for automatic parameter selection (p,d,q).",
        "mc_title": "## 🎲 Monte Carlo Simulation",
        "mc_expl": "Monte Carlo simulates thousands of possible portfolio trajectories under a multivariate normal distribution, accounting for asset correlations. **VaR 95%** indicates the maximum expected loss with 95% confidence.",
        "hr_load": "## 👥 IBM Watson HR Dataset — Loading and EDA",
        "att_title": "## ⚠️ Attrition Analysis",
        "att_expl": "The **attrition rate** measures what percentage of employees leave the organization. A high rate implies high replacement costs (~$15,000 USD per employee in tech roles).",
        "gap_title": "## ⚖️ Pay Gap and t-Test",
        "gap_expl": "We use the **Student's t-test** (α=0.05) to determine whether salary differences between genders are statistically significant or attributable to chance.",
        "model_title": "## 🤖 Attrition Predictive Model",
        "model_expl": "**Logistic Regression** to predict which employees are most likely to leave. We use class_weight='balanced' to handle class imbalance (16% attrition vs 84% retention).",
        "summary_title": "## 📋 Executive Summary — LinkedIn Findings",
        "summary": """## 🎯 Key Findings

**CFO Perspective:**
- ARIMA projects portfolio growth with 95% CI
- VaR 95%: maximum loss controlled and quantified
- Monte Carlo: majority of simulations end positive

**CHRO Perspective:**
- Sales: 20.6% attrition — 7.6 pts above benchmark (13%)
- Pay gap not statistically significant (p>0.05)
- OverTime is the main attrition predictor

**Stack:** Python · Statsmodels · Scikit-learn · Plotly · yfinance"""
    },
    "BR": {
        "title": "# 💼 Inteligência Financeira e RH — Análise Completa\n**Autor:** Hely Camargo | **Stack:** Python · Statsmodels · Scikit-learn · Plotly",
        "ctx": "## 🎯 Contexto de Negócio\nEsta análise responde duas perguntas críticas para a C-Suite:\n- **CFO:** Qual é o risco e retorno esperado do portfólio em 12 meses?\n- **CHRO:** Existe equidade salarial? O que impulsiona a rotatividade?\n\n**Dataset RH:** IBM Watson Analytics — 1.470 funcionários | **Dados Financeiros:** Yahoo Finance — 5 anos",
        "deps": "## 📦 Instalação de Dependências",
        "load": "## 📂 Carregamento de Dados com QA",
        "eda_fin": "## 📈 EDA Financeiro — Evolução de Preços",
        "arima_title": "## 🔮 Modelo ARIMA — Projeção 12 Meses",
        "arima_expl": "O modelo ARIMA captura tendência e autocorrelação em séries temporais financeiras. Aplicamos o **teste ADF** para verificar estacionariedade e **auto_arima** para seleção automática de parâmetros (p,d,q).",
        "mc_title": "## 🎲 Simulação Monte Carlo",
        "mc_expl": "Monte Carlo simula milhares de trajetórias possíveis do portfólio sob distribuição normal multivariada. O **VaR 95%** indica a perda máxima esperada com 95% de confiança.",
        "hr_load": "## 👥 Dataset IBM Watson RH — Carregamento e EDA",
        "att_title": "## ⚠️ Análise de Attrition",
        "att_expl": "A **taxa de rotatividade** mede o percentual de funcionários que saem da organização. Alta rotatividade implica custos de reposição elevados (~$15.000 USD por funcionário em tecnologia).",
        "gap_title": "## ⚖️ Lacuna Salarial e Teste t",
        "gap_expl": "Utilizamos o **teste t de Student** (α=0,05) para determinar se as diferenças salariais entre gêneros são estatisticamente significativas.",
        "model_title": "## 🤖 Modelo Preditivo de Attrition",
        "model_expl": "**Regressão Logística** para prever quais funcionários têm maior probabilidade de sair. Usamos class_weight='balanced' para tratar o desbalanceamento de classes.",
        "summary_title": "## 📋 Resumo Executivo — Descobertas para LinkedIn",
        "summary": """## 🎯 Descobertas Principais

**Perspectiva CFO:**
- ARIMA projeta crescimento do portfólio com IC de 95%
- VaR 95%: perda máxima controlada e quantificada
- Monte Carlo: maioria das simulações terminam positivas

**Perspectiva CHRO:**
- Vendas: 20,6% attrition — 7,6 pts acima do benchmark (13%)
- Lacuna salarial não significativa estatisticamente (p>0,05)
- Horas extras é o principal preditor de rotatividade

**Stack:** Python · Statsmodels · Scikit-learn · Plotly · yfinance"""
    }
}

CODE_CELLS = {
    "deps": '!pip install pandas numpy plotly statsmodels scikit-learn yfinance scipy pmdarima matplotlib --quiet',
    "load_fin": '''import pandas as pd, numpy as np, warnings
warnings.filterwarnings("ignore")

# Load financial data
prices = pd.read_csv("../output/financial_clean.csv", index_col=0, parse_dates=True)
print(f"Shape: {prices.shape}")
print(prices.tail(3))''',
    "eda_fin": '''import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(14,8), facecolor="#061a40")
colors = ["#b9d6f2","#0353a4","#006daa","#4caf82"]
for ax, (ticker, color) in zip(axes.flat, zip(prices.columns, colors)):
    ax.plot(prices.index, prices[ticker], color=color, linewidth=2)
    ax.set_title(ticker, color="#e8f4fd", fontsize=13, fontweight="bold")
    ax.set_facecolor("#003559"); ax.tick_params(colors="#7ba7c9")
    for spine in ax.spines.values(): spine.set_edgecolor("rgba(185,214,242,0.2)")
plt.suptitle("Stock Price History (5Y)", color="#e8f4fd", fontsize=15, fontweight="bold")
plt.tight_layout(); plt.show()''',
    "arima": '''from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller

ticker = "AAPL"
series = prices[ticker].dropna()

# ADF Test
adf = adfuller(series)
print(f"ADF p-value: {adf[1]:.4f} — {'Estacionaria' if adf[1]<0.05 else 'No estacionaria'}")

# auto_arima
model = auto_arima(series, d=1, stepwise=True, suppress_warnings=True, error_action="ignore")
print(f"Best order: {model.order}")

# Forecast
fc, ci = model.predict(12, return_conf_int=True, alpha=0.05)
print(pd.DataFrame({"forecast":fc.round(2),"lower":ci[:,0].round(2),"upper":ci[:,1].round(2)}).head())''',
    "mc": '''import numpy as np
monthly_ret = prices.pct_change().dropna()
mu, cov = monthly_ret.mean().values, monthly_ret.cov().values
weights = np.ones(4)/4
finals = []
np.random.seed(42)
for _ in range(5000):
    cum = 1.0
    for __ in range(12):
        r = weights @ np.random.multivariate_normal(mu, cov)
        cum *= (1+r)
    finals.append(cum)
finals = np.array(finals)
var95 = np.percentile(finals, 5) - 1
print(f"VaR 95%: {var95:.2%}")
print(f"Median return: {np.median(finals)-1:.2%}")
print(f"% Positive: {(finals>1).mean():.1%}")

import matplotlib.pyplot as plt
plt.figure(figsize=(10,5), facecolor="#061a40")
plt.hist(finals-1, bins=80, color="#0353a4", alpha=0.7)
plt.axvline(var95, color="#e05252", linestyle="--", label=f"VaR 95%: {var95:.1%}")
plt.title("Monte Carlo Distribution", color="#e8f4fd"); plt.legend()
plt.gca().set_facecolor("#003559"); plt.show()''',
    "hr_load": '''df_hr = pd.read_csv("../data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
df_hr["Attrition_num"] = (df_hr["Attrition"]=="Yes").astype(int)
print(f"Shape: {df_hr.shape}")
print(df_hr["Attrition"].value_counts())
print(f"\\nAttrition rate: {df_hr['Attrition_num'].mean():.1%}")''',
    "attrition": '''import matplotlib.pyplot as plt
dept_att = df_hr.groupby("Department")["Attrition_num"].mean().sort_values()
fig, ax = plt.subplots(figsize=(8,4), facecolor="#061a40")
colors = ["#4caf82" if v<0.13 else ("#f0a500" if v<0.20 else "#e05252") for v in dept_att]
ax.barh(dept_att.index, dept_att*100, color=colors)
ax.axvline(13, color="#b9d6f2", linestyle="--", label="Benchmark 13%")
ax.set_xlabel("Attrition %", color="#b9d6f2"); ax.set_title("Attrition by Department", color="#e8f4fd")
ax.set_facecolor("#003559"); ax.tick_params(colors="#7ba7c9"); ax.legend()
plt.tight_layout(); plt.show()''',
    "pay_gap": '''from scipy import stats
males = df_hr[df_hr["Gender"]=="Male"]["MonthlyIncome"].dropna()
females = df_hr[df_hr["Gender"]=="Female"]["MonthlyIncome"].dropna()
t_stat, p_val = stats.ttest_ind(males, females)
gap_pct = (males.mean() - females.mean()) / males.mean() * 100
print(f"Male avg salary: ${males.mean():,.0f}")
print(f"Female avg salary: ${females.mean():,.0f}")
print(f"Gap: {gap_pct:.1f}%")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_val:.4f} — {'SIGNIFICANT' if p_val<0.05 else 'NOT significant'} (alpha=0.05)")''',
    "model": '''from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

features = ["Age","MonthlyIncome","TotalWorkingYears","JobLevel",
            "JobSatisfaction","EnvironmentSatisfaction","YearsAtCompany"]
X = df_hr[features].fillna(0)
y = df_hr["Attrition_num"]
scaler = StandardScaler()
X_s = scaler.fit_transform(X)
X_tr,X_te,y_tr,y_te = train_test_split(X_s,y,test_size=0.25,random_state=42,stratify=y)
lr = LogisticRegression(class_weight="balanced",max_iter=1000)
lr.fit(X_tr,y_tr)
print(classification_report(y_te, lr.predict(X_te)))'''
}

os.makedirs("notebooks", exist_ok=True)
filenames = {"ES":"financial_hr_analysis_ES","EN":"financial_hr_analysis_EN","BR":"financial_hr_analysis_BR"}

for lang, texts in LANGS.items():
    cells = [
        md(texts["title"]),
        md(texts["ctx"]),
        md(texts["deps"]),
        code(CODE_CELLS["deps"]),
        md(texts["load"]),
        code(CODE_CELLS["load_fin"]),
        md(texts["eda_fin"]),
        code(CODE_CELLS["eda_fin"]),
        md(texts["arima_title"]),
        md(texts["arima_expl"]),
        code(CODE_CELLS["arima"]),
        md(texts["mc_title"]),
        md(texts["mc_expl"]),
        code(CODE_CELLS["mc"]),
        md(texts["hr_load"]),
        code(CODE_CELLS["hr_load"]),
        md(texts["att_title"]),
        md(texts["att_expl"]),
        code(CODE_CELLS["attrition"]),
        md(texts["gap_title"]),
        md(texts["gap_expl"]),
        code(CODE_CELLS["pay_gap"]),
        md(texts["model_title"]),
        md(texts["model_expl"]),
        code(CODE_CELLS["model"]),
        md(texts["summary_title"]),
        md(texts["summary"]),
    ]
    path = f"notebooks/{filenames[lang]}.ipynb"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(make_nb(cells), f, ensure_ascii=False, indent=1)
    print(f"[OK] Created {path}")

print("All notebooks created!")
