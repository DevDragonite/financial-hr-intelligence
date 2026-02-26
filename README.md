# Financial & HR Intelligence Center

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14-4B8BBE?style=flat-square)](https://www.statsmodels.org)
[![yfinance](https://img.shields.io/badge/yfinance-1.2-00B4D8?style=flat-square)](https://pypi.org/project/yfinance)
[![Plotly](https://img.shields.io/badge/Plotly-6.5-3D9970?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)

> **Executive Intelligence Center** bridging CFO financial risk analysis with CHRO people analytics, all in a single evidence-based dashboard.

<p align="center">
  <img src="docs/screenshot.png" alt="Dashboard Preview" width="800"/>
</p>

---

## 🎯 Problem Statement

Organizations operate with two parallel intelligence needs that rarely communicate:

- **CFO** needs: portfolio risk quantification, 12-month return projections, scenario planning
- **CHRO** needs: attrition predictors, pay equity validation, workforce diversity metrics

This project unifies both into one data-driven executive dashboard.

---

## ✨ Features

### 💰 Financial Intelligence (CFO)
- **ARIMA Forecasting** — Auto-selected (p,d,q) via ADF test + pmdarima, 12-month projection with 80%/95% CI
- **Monte Carlo Simulation** — 5,000+ portfolio simulations with VaR 95%, CVaR, and scenario percentiles
- **Asset Correlation Heatmap** — Identifies diversification opportunities
- **yfinance Integration** — 5 years of real AAPL, MSFT, GOOGL, AMZN data (synthetic fallback if offline)

### 👥 People Analytics (CHRO)
- **Attrition Analysis** — Department breakdown, Spearman correlation with 10+ features, Logistic Regression
- **Pay Equity (t-Test)** — Student's t-test by gender & department with statistical significance annotation
- **Diversity Dashboard** — Gender distribution by dept/level + satisfaction heatmap
- **Predictive Model** — Logistic Regression identifying at-risk employees

### 🌐 Multilingual
- Full ES / EN / BR support — every label, insight, and conclusion translates dynamically

---

## 📁 Project Structure

```
financial-hr-intelligence/
├── app.py                    ← Streamlit main application
├── config.py                 ← Deep Navy color palette + Plotly template
├── translations.py           ← Full ES/EN/BR i18n dictionary
├── financial_pipeline.py     ← ARIMA, Monte Carlo, yfinance
├── hr_pipeline.py            ← Attrition, pay gap, diversity
├── test_imports.py           ← QA import validation
├── generate_notebooks.py     ← Notebook generator script
├── notebooks/
│   ├── financial_hr_analysis_ES.ipynb
│   ├── financial_hr_analysis_EN.ipynb
│   └── financial_hr_analysis_BR.ipynb
├── data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
├── output/
│   ├── financial_clean.csv
│   ├── hr_clean.csv
│   ├── monte_carlo_results.csv
│   ├── arima_forecast.csv
│   └── financial_hr_qa_log.txt
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/DevDragonite/financial-hr-intelligence.git
cd financial-hr-intelligence
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run QA validation
```bash
python test_imports.py
# Expected: ✅ Todos los imports pasaron.
```

### 5. Generate pipeline data
```bash
python financial_pipeline.py
python hr_pipeline.py
```

### 6. Generate notebooks
```bash
python generate_notebooks.py
```

### 7. Launch the app
```bash
streamlit run app.py
```

---

## 🔍 Key Findings

### Financial (CFO)
1. **ARIMA Forecast** — MSFT projects highest 12M return in the portfolio with controlled volatility
2. **Monte Carlo Risk** — VaR 95% = ~-18.8%; 75%+ of simulations end in positive territory

### HR (CHRO)
3. **Attrition Hotspot** — Sales dept: 20.6% attrition vs 13% industry benchmark (7.6 pts above)
4. **Pay Equity** — Global salary gap not statistically significant (p=0.222, α=0.05); OverTime is the #1 attrition predictor (Spearman r=0.25)

---

## 📌 Methodology Note

| Component | Source | Method |
|-----------|--------|--------|
| Stock data | Yahoo Finance (5Y monthly) | yfinance API + synthetic fallback |
| ARIMA | ADF stationarity test → auto_arima | pmdarima, IC: AIC |
| Monte Carlo | Multivariate normal distribution | NumPy, n=5,000 simulations |
| HR Dataset | IBM Watson HR Analytics | 1,470 employees, 35 features |
| Pay gap | Student's t-test | scipy.stats, α=0.05 |
| Attrition model | Logistic Regression | scikit-learn, class_weight=balanced |

---

## 👤 Author

**Developed by Hely Camargo**
Python · Statsmodels · Scikit-learn · Plotly · Streamlit

🔗 [GitHub](https://github.com/DevDragonite/financial-hr-intelligence)
