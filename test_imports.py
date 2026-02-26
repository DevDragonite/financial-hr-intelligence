import datetime
import traceback


def test_imports():
    packages = [
        "pandas", "numpy", "plotly", "streamlit",
        "sklearn", "statsmodels", "yfinance",
        "scipy", "openpyxl", "pmdarima", "matplotlib"
    ]
    success = True
    log_file = "output/financial_hr_qa_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    import os
    os.makedirs("output", exist_ok=True)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n--- PASO 0 QA: {timestamp} ---\n")
        for pkg in packages:
            try:
                __import__(pkg)
                f.write(f"[OK] {pkg} importado correctamente.\n")
            except ImportError as e:
                f.write(f"[ERROR] {pkg}: {e}\n")
                f.write(traceback.format_exc())
                success = False
    return success


if __name__ == "__main__":
    if test_imports():
        print("✅ Todos los imports pasaron.")
    else:
        print("❌ Algunos imports fallaron. Ver output/financial_hr_qa_log.txt")
        exit(1)
