# financial_pipeline.py — ARIMA + Monte Carlo + yfinance
"""
Pipeline financiero:
  1. Descarga datos históricos con yfinance (fallback sintético)
  2. Modelos ARIMA individuales por ticker con auto_arima
  3. Simulación Monte Carlo del portfolio completo

Exporta:
  data/financial_data.csv
  output/financial_clean.csv
  output/arima_forecast.csv
  output/monte_carlo_results.csv
"""

import os
import datetime
import traceback
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

LOG_FILE = "output/financial_hr_qa_log.txt"
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]


def _log(msg: str):
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] FINANCIAL | {msg}\n")
    print(msg)


# ─────────────────────────────────────────────────────────────
# STEP 1: DESCARGA / DATOS SINTÉTICOS
# ─────────────────────────────────────────────────────────────
def _synthetic_prices(ticker: str, periods: int = 60) -> pd.Series:
    """Genera serie de precios sintéticos si yfinance falla."""
    np.random.seed(abs(hash(ticker)) % (2**31))
    base = {"AAPL": 150, "MSFT": 280, "GOOGL": 130, "AMZN": 170}.get(ticker, 100)
    trend = 0.008
    seasonality = 0.05 * np.sin(np.linspace(0, 4 * np.pi, periods))
    noise = np.random.normal(0, 0.04, periods)
    log_returns = trend + seasonality / periods + noise
    prices = base * np.exp(np.cumsum(log_returns))
    idx = pd.date_range(
        end=datetime.date.today(), periods=periods, freq="MS"
    )
    return pd.Series(prices, index=idx, name=ticker)


def load_financial_data() -> pd.DataFrame:
    """Descarga 5 años de datos mensuales; fallback sintético si falla."""
    os.makedirs("data", exist_ok=True)
    cache = "data/financial_data.csv"

    try:
        import yfinance as yf
        end = datetime.date.today()
        start = end - datetime.timedelta(days=5 * 365)
        raw = yf.download(
            TICKERS, start=start.isoformat(), end=end.isoformat(),
            interval="1mo", auto_adjust=True, progress=False
        )
        close = raw["Close"] if "Close" in raw.columns else raw.xs("Close", axis=1, level=0)
        close = close.dropna()
        if close.empty or len(close) < 10:
            raise ValueError("Datos insuficientes de yfinance.")
        close.index = pd.to_datetime(close.index)
        close.index = close.index.tz_localize(None)
        close.to_csv(cache)
        _log(f"[OK] yfinance: {len(close)} filas descargadas para {TICKERS}.")
        return close

    except Exception as e:
        _log(f"[WARN] yfinance falló: {e}. Usando datos sintéticos.")
        series = {t: _synthetic_prices(t) for t in TICKERS}
        df = pd.DataFrame(series)
        df.index = pd.to_datetime(df.index)
        df.to_csv(cache)
        _log(f"[OK] Sintético: {len(df)} filas generadas.")
        return df


# ─────────────────────────────────────────────────────────────
# STEP 2: MODELO ARIMA
# ─────────────────────────────────────────────────────────────
def run_arima_forecast(prices: pd.DataFrame, n_forecast: int = 12) -> pd.DataFrame:
    """
    Test ADF → auto_arima → forecast 12 meses + IC 80/95%.
    Retorna DataFrame con columnas: ticker, date, forecast,
      lower_80, upper_80, lower_95, upper_95
    """
    from pmdarima import auto_arima
    from statsmodels.tsa.stattools import adfuller

    results = []

    for ticker in prices.columns:
        series = prices[ticker].dropna()
        if len(series) < 12:
            _log(f"[WARN] {ticker}: serie muy corta ({len(series)} obs). Skip ARIMA.")
            continue

        try:
            # ADF Test
            adf_result = adfuller(series)
            adf_pval = adf_result[1]
            d_param = 0 if adf_pval < 0.05 else 1
            _log(f"[OK] {ticker}: ADF p={adf_pval:.4f} → d={d_param}")

            # auto_arima
            model = auto_arima(
                series, d=d_param, start_p=0, start_q=0,
                max_p=3, max_q=3, seasonal=False,
                stepwise=True, suppress_warnings=True,
                error_action="ignore", information_criterion="aic",
            )

            # Forecast
            fc_80 = model.predict(n_periods=n_forecast, return_conf_int=True, alpha=0.20)
            fc_95 = model.predict(n_periods=n_forecast, return_conf_int=True, alpha=0.05)

            forecast_vals = fc_80[0]
            ci_80 = fc_80[1]
            ci_95 = fc_95[1]

            future_idx = pd.date_range(
                start=series.index[-1] + pd.DateOffset(months=1),
                periods=n_forecast, freq="MS"
            )

            for i in range(n_forecast):
                results.append({
                    "ticker": ticker,
                    "date": future_idx[i],
                    "forecast": round(float(forecast_vals[i]), 4),
                    "lower_80": round(float(ci_80[i][0]), 4),
                    "upper_80": round(float(ci_80[i][1]), 4),
                    "lower_95": round(float(ci_95[i][0]), 4),
                    "upper_95": round(float(ci_95[i][1]), 4),
                })

            _log(f"[OK] ARIMA {ticker}: {model.order} → forecast 12M ok.")

        except Exception as e:
            _log(f"[ERROR] ARIMA {ticker}: {e}")
            _log(traceback.format_exc())

    df_fc = pd.DataFrame(results)
    os.makedirs("output", exist_ok=True)
    df_fc.to_csv("output/arima_forecast.csv", index=False)
    _log(f"[QA] arima_forecast.csv: {len(df_fc)} filas. Tickers: {df_fc['ticker'].unique().tolist()}")
    return df_fc


# ─────────────────────────────────────────────────────────────
# STEP 3: MONTE CARLO
# ─────────────────────────────────────────────────────────────
def run_monte_carlo(prices: pd.DataFrame, n_simulations: int = 5000, n_months: int = 12) -> dict:
    """
    Simulación Monte Carlo del portfolio igualitario.
    Retorna dict con métricas y DataFrame de simulaciones.
    """
    monthly_returns = prices.pct_change().dropna()
    mu = monthly_returns.mean().values          # vector de medias
    cov = monthly_returns.cov().values          # matriz de covarianza

    # Inversión inicial unitaria por ticker
    n_assets = len(prices.columns)
    weights = np.ones(n_assets) / n_assets

    portfolio_finals = []
    path_records = []

    np.random.seed(42)
    for sim in range(n_simulations):
        cumulative = 1.0
        path = [1.0]
        for _ in range(n_months):
            # Retornos correlacionados mediante Cholesky
            sample = np.random.multivariate_normal(mu, cov)
            portfolio_return = weights @ sample
            cumulative *= (1 + portfolio_return)
            path.append(round(cumulative, 6))
        portfolio_finals.append(cumulative)
        if sim < 500:  # guardar primeras 500 trayectorias para fan chart
            path_records.append(path)

    finals = np.array(portfolio_finals)

    # Métricas de riesgo
    var_95 = float(np.percentile(finals, 5))          # VaR 95%
    cvar = float(finals[finals <= var_95].mean())     # CVaR
    p5  = float(np.percentile(finals, 5))
    p50 = float(np.median(finals))
    p95 = float(np.percentile(finals, 95))
    pct_positive = float((finals > 1.0).mean() * 100)

    metrics = {
        "var_95":       round(var_95 - 1, 4),
        "cvar":         round(cvar - 1, 4),
        "worst_case":   round(p5 - 1, 4),
        "base_case":    round(p50 - 1, 4),
        "best_case":    round(p95 - 1, 4),
        "pct_positive": round(pct_positive, 2),
        "n_simulations": n_simulations,
    }
    _log(f"[OK] Monte Carlo: VaR95={metrics['var_95']:.2%}, CVaR={metrics['cvar']:.2%}, "
         f"P50={metrics['base_case']:.2%}, P95={metrics['best_case']:.2%}, "
         f"%Positivas={metrics['pct_positive']:.1f}%")

    # Guardar distribución de finales
    df_mc = pd.DataFrame({
        "final_value": finals,
        "return_pct": (finals - 1) * 100
    })
    df_mc.to_csv("output/monte_carlo_results.csv", index=False)
    _log(f"[QA] monte_carlo_results.csv: {len(df_mc)} filas.")

    return {
        "metrics": metrics,
        "finals": finals,
        "paths": path_records,
        "tickers": list(prices.columns),
    }


# ─────────────────────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────
def run_financial_pipeline(n_simulations: int = 5000) -> dict:
    """
    Ejecuta el pipeline completo:
      load_financial_data → run_arima_forecast → run_monte_carlo
    Retorna dict con todos los resultados para uso en Streamlit.
    """
    _log("=" * 60)
    _log("INICIANDO PIPELINE FINANCIERO")
    _log("=" * 60)

    # 1. Cargar precios
    prices = load_financial_data()
    os.makedirs("output", exist_ok=True)
    prices.to_csv("output/financial_clean.csv")
    _log(f"[OK] financial_clean.csv guardado: {prices.shape}")

    # 2. ARIMA
    arima_df = run_arima_forecast(prices)

    # 3. Monte Carlo
    mc_results = run_monte_carlo(prices, n_simulations=n_simulations)

    # 4. Retornos históricos mensuales para correlación
    monthly_returns = prices.pct_change().dropna()

    _log("PIPELINE FINANCIERO COMPLETADO ✓")
    _log("=" * 60)

    return {
        "prices": prices,
        "monthly_returns": monthly_returns,
        "arima_forecast": arima_df,
        "mc_results": mc_results,
    }


if __name__ == "__main__":
    results = run_financial_pipeline(n_simulations=5000)
    print("\n--- QA FINAL ---")
    print(f"Precios: {results['prices'].shape}")
    print(f"ARIMA filas: {len(results['arima_forecast'])}")
    print(f"MC métricas: {results['mc_results']['metrics']}")
