# hr_pipeline.py — People Analytics Pipeline
"""
Pipeline HR Analytics con dataset IBM Watson HR Attrition:
  1. Carga y QA del dataset
  2. Análisis de attrition (Logistic Regression + correlaciones)
  3. Análisis de brecha salarial (prueba t)
  4. Análisis de diversidad

Exporta:
  output/hr_clean.csv
"""

import os
import datetime
import traceback
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats

LOG_FILE = "output/financial_hr_qa_log.txt"
DATA_PATH = "data/WA_Fn-UseC_-HR-Employee-Attrition.csv"


def _log(msg: str):
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] HR | {msg}\n")
    print(msg)


# ─────────────────────────────────────────────────────────────
# STEP 1: CARGA Y QA
# ─────────────────────────────────────────────────────────────
def load_hr_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    _log(f"[OK] Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas.")

    # QA inmediato
    nulls = df.isnull().sum().sum()
    _log(f"[QA] Nulos totales: {nulls}")

    attrition_vc = df["Attrition"].value_counts().to_dict()
    _log(f"[QA] Attrition distribution: {attrition_vc}")

    # Mapear Attrition a binario
    df["Attrition_num"] = (df["Attrition"] == "Yes").astype(int)

    # Columnas requeridas
    required = [
        "Attrition", "Age", "Department", "Gender", "JobLevel",
        "MonthlyIncome", "OverTime", "TotalWorkingYears", "YearsAtCompany",
        "JobSatisfaction", "EnvironmentSatisfaction"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        _log(f"[WARN] Columnas faltantes: {missing}")

    return df


# ─────────────────────────────────────────────────────────────
# STEP 2: ANÁLISIS DE ATTRITION
# ─────────────────────────────────────────────────────────────
def analyze_attrition(df: pd.DataFrame) -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from sklearn.preprocessing import StandardScaler

    # Tasa global
    global_rate = df["Attrition_num"].mean()
    _log(f"[OK] Tasa global de attrition: {global_rate:.1%}")

    # Por departamento
    dept_rates = df.groupby("Department")["Attrition_num"].mean().reset_index()
    dept_rates.columns = ["Department", "Attrition_Rate"]
    dept_rates["Attrition_Rate_Pct"] = (dept_rates["Attrition_Rate"] * 100).round(1)
    _log(f"[OK] Attrition por dpto:\n{dept_rates.to_string(index=False)}")

    # Correlación Spearman con variables numéricas
    numeric_cols = [
        "Age", "MonthlyIncome", "TotalWorkingYears", "YearsAtCompany",
        "JobLevel", "JobSatisfaction", "EnvironmentSatisfaction",
        "DistanceFromHome", "NumCompaniesWorked", "YearsInCurrentRole",
        "YearsSinceLastPromotion", "WorkLifeBalance", "PerformanceRating"
    ]
    numeric_cols = [c for c in numeric_cols if c in df.columns]

    corr_results = []
    for col in numeric_cols:
        r, p = stats.spearmanr(df[col].fillna(df[col].median()), df["Attrition_num"])
        corr_results.append({"Feature": col, "Spearman_r": round(r, 4), "p_value": round(p, 4)})

    # OverTime binario
    if "OverTime" in df.columns:
        df["OverTime_num"] = (df["OverTime"] == "Yes").astype(int)
        r, p = stats.spearmanr(df["OverTime_num"], df["Attrition_num"])
        corr_results.append({"Feature": "OverTime", "Spearman_r": round(r, 4), "p_value": round(p, 4)})

    corr_df = pd.DataFrame(corr_results).sort_values("Spearman_r", key=abs, ascending=False)
    _log(f"[OK] Top factores attrition:\n{corr_df.head(10).to_string(index=False)}")

    # Logistic Regression
    feature_cols = [c["Feature"] for c in corr_results[:10]]
    feature_df = df[feature_cols + ["Attrition_num"]].dropna()

    X = feature_df[feature_cols]
    y = feature_df["Attrition_num"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.25, random_state=42, stratify=y
    )

    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)

    model_metrics = {
        "accuracy":  round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "recall":    round(recall_score(y_test, y_pred, zero_division=0), 4),
        "f1":        round(f1_score(y_test, y_pred, zero_division=0), 4),
    }
    _log(f"[OK] Logistic Regression: {model_metrics}")
    if model_metrics["accuracy"] < 0.70:
        _log("[WARN] Accuracy < 70%. Revisar features.")

    # Coeficientes del modelo
    coef_df = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": lr.coef_[0]
    }).sort_values("Coefficient", key=abs, ascending=False)

    return {
        "global_rate": global_rate,
        "dept_rates": dept_rates,
        "correlations": corr_df,
        "model_metrics": model_metrics,
        "coef_df": coef_df,
    }


# ─────────────────────────────────────────────────────────────
# STEP 3: BRECHA SALARIAL
# ─────────────────────────────────────────────────────────────
def analyze_pay_gap(df: pd.DataFrame) -> dict:
    # Salario promedio por género
    gender_salary = df.groupby("Gender")["MonthlyIncome"].agg(["mean", "median", "std", "count"])
    _log(f"[OK] Salario por género:\n{gender_salary.to_string()}")

    m_sal = gender_salary.loc["Male", "mean"] if "Male" in gender_salary.index else np.nan
    f_sal = gender_salary.loc["Female", "mean"] if "Female" in gender_salary.index else np.nan
    global_gap_pct = round((m_sal - f_sal) / m_sal * 100, 2) if not np.isnan(m_sal) else 0
    global_gap_abs = round(m_sal - f_sal, 2) if not np.isnan(m_sal) else 0

    # Prueba t global
    males = df[df["Gender"] == "Male"]["MonthlyIncome"].dropna()
    females = df[df["Gender"] == "Female"]["MonthlyIncome"].dropna()
    t_stat, p_val = stats.ttest_ind(males, females)
    _log(f"[OK] Prueba t global: t={t_stat:.4f}, p={p_val:.4f}, gap={global_gap_pct:.1f}%")

    # Por departamento
    dept_gap = []
    for dept in df["Department"].unique():
        sub = df[df["Department"] == dept]
        m = sub[sub["Gender"] == "Male"]["MonthlyIncome"].dropna()
        f = sub[sub["Gender"] == "Female"]["MonthlyIncome"].dropna()
        if len(m) < 5 or len(f) < 5:
            continue
        t, p = stats.ttest_ind(m, f)
        gap_pct = (m.mean() - f.mean()) / m.mean() * 100
        dept_gap.append({
            "Department": dept,
            "Male_Avg": round(m.mean(), 2),
            "Female_Avg": round(f.mean(), 2),
            "Gap_Pct": round(gap_pct, 2),
            "Gap_Abs": round(m.mean() - f.mean(), 2),
            "t_stat": round(t, 4),
            "p_value": round(p, 4),
            "Significant": p < 0.05,
        })

    dept_gap_df = pd.DataFrame(dept_gap)
    _log(f"[OK] Brecha por dpto:\n{dept_gap_df.to_string(index=False)}")

    return {
        "global_gap_pct": global_gap_pct,
        "global_gap_abs": global_gap_abs,
        "global_pvalue": round(p_val, 4),
        "global_tstat": round(t_stat, 4),
        "gender_salary": gender_salary.reset_index(),
        "dept_gap": dept_gap_df,
    }


# ─────────────────────────────────────────────────────────────
# STEP 4: DIVERSIDAD
# ─────────────────────────────────────────────────────────────
def analyze_diversity(df: pd.DataFrame) -> dict:
    # Distribución género por departamento
    gender_dept = df.groupby(["Department", "Gender"]).size().unstack(fill_value=0)
    gender_dept_pct = gender_dept.div(gender_dept.sum(axis=1), axis=0) * 100
    _log(f"[OK] Distribución género por dpto:\n{gender_dept_pct.to_string()}")

    # Satisfacción por género
    satisfaction_gender = df.groupby("Gender")[
        ["JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance"]
    ].mean().round(2)
    _log(f"[OK] Satisfacción por género:\n{satisfaction_gender.to_string()}")

    # Satisfacción por departamento (para heatmap)
    satisfaction_dept = df.groupby("Department")[
        ["JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance"]
    ].mean().round(2)

    return {
        "gender_dept": gender_dept,
        "gender_dept_pct": gender_dept_pct,
        "satisfaction_gender": satisfaction_gender,
        "satisfaction_dept": satisfaction_dept,
    }


# ─────────────────────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────
def run_hr_pipeline() -> dict:
    """
    Ejecuta el pipeline HR completo y retorna dict con todos
    los resultados para uso en Streamlit.
    """
    _log("=" * 60)
    _log("INICIANDO PIPELINE HR ANALYTICS")
    _log("=" * 60)

    df = load_hr_data()

    attrition_results = analyze_attrition(df)
    pay_gap_results   = analyze_pay_gap(df)
    diversity_results = analyze_diversity(df)

    # Guardar CSV limpio
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/hr_clean.csv", index=False)
    _log(f"[OK] hr_clean.csv guardado: {df.shape}")

    _log("PIPELINE HR COMPLETADO ✓")
    _log("=" * 60)

    # QA p-value
    pval = pay_gap_results["global_pvalue"]
    _log(f"[QA] p-value prueba t global: {pval} — "
         f"{'SIGNIFICATIVO' if pval < 0.05 else 'NO significativo'} (α=0.05)")

    acc = attrition_results["model_metrics"]["accuracy"]
    _log(f"[QA] Accuracy Logistic Regression: {acc:.2%} — "
         f"{'OK' if acc >= 0.70 else 'WARN: <70%'}")

    return {
        "df": df,
        "attrition": attrition_results,
        "pay_gap": pay_gap_results,
        "diversity": diversity_results,
    }


if __name__ == "__main__":
    results = run_hr_pipeline()
    print("\n--- QA FINAL ---")
    print(f"Dataset shape: {results['df'].shape}")
    print(f"Global attrition: {results['attrition']['global_rate']:.1%}")
    print(f"Pay gap global: {results['pay_gap']['global_gap_pct']:.1f}%  p={results['pay_gap']['global_pvalue']}")
    print(f"Model accuracy: {results['attrition']['model_metrics']['accuracy']:.2%}")
