import logging
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# ============================================================
# PATH FIX → ALWAYS WORKS IN VS CODE
# ============================================================
BASE_DIR = Path(__file__).resolve().parent        # D:\CODES\PYTHON
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# Auto-create folders
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Logging setup
LOG_FILE = LOG_DIR / "ingestion.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler())

# ============================================================
# TASK 1: INGESTION + VALIDATION
# ============================================================

TIMESTAMP_COLS = ["timestamp", "time", "datetime", "date"]
KWH_COLS = ["kwh", "energy", "value", "consumption"]

def read_single_csv(path: Path):
    """Reads a CSV and extracts timestamp + kwh columns safely."""
    try:
        df = pd.read_csv(path, on_bad_lines="skip")
    except Exception as e:
        logging.error(f"Error reading {path}: {e}")
        return None

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    print("DEBUG columns:", df.columns.tolist())

    ts_col = next((c for c in TIMESTAMP_COLS if c in df.columns), None)
    kwh_col = next((c for c in KWH_COLS if c in df.columns), None)

    if not ts_col or not kwh_col:
        logging.error(f"Missing timestamp/kwh in {path}. Columns: {df.columns.tolist()}")
        return None

    df.rename(columns={ts_col: "timestamp", kwh_col: "kwh"}, inplace=True)

    # Convert types
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")

    df = df.dropna(subset=["timestamp", "kwh"])

    return df


def ingest_all_data():
    """Loads all CSV files."""
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        logging.error("No CSV files found in /data folder!")
        return pd.DataFrame()

    frames = []
    for file in csv_files:
        logging.info(f"Reading {file.name}")
        df = read_single_csv(file)
        if df is None:
            continue

        # Assign building name from filename
        building = file.stem.split("_")[0]
        df["building"] = building

        frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


# ============================================================
# TASK 2: AGGREGATION LOGIC
# ============================================================

def calculate_daily_totals(df):
    df = df.copy().set_index("timestamp")
    return df.groupby("building").resample("D")["kwh"].sum().unstack(0).fillna(0)

def calculate_weekly_aggregates(df):
    df = df.copy().set_index("timestamp")
    return df.groupby("building").resample("W")["kwh"].sum().unstack(0).fillna(0)

def building_wise_summary(df):
    return df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])


# ============================================================
# TASK 4: VISUAL OUTPUT
# ============================================================

def create_dashboard(daily, weekly, df):
    fig, axes = plt.subplots(3, 1, figsize=(12, 14))

    daily.plot(ax=axes[0])
    axes[0].set_title("Daily Consumption")

    weekly.mean().plot(kind="bar", ax=axes[1])
    axes[1].set_title("Avg Weekly Consumption")

    # Scatter
    h = df.copy()
    h["hour"] = h["timestamp"].dt.floor("H")
    axes[2].scatter(h["hour"], h["kwh"])
    axes[2].set_title("Hourly Consumption")
    axes[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "dashboard.png")
    plt.close()


# ============================================================
# TASK 5: SAVE OUTPUTS
# ============================================================

def create_outputs(df, summary):
    df.to_csv(OUTPUT_DIR / "cleaned_energy_data.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "building_summary.csv")

    total = df["kwh"].sum()
    max_b = summary["sum"].idxmax()

    with open(OUTPUT_DIR / "summary.txt", "w") as f:
        f.write(
            f"TOTAL CONSUMPTION: {total}\n"
            f"HIGHEST BUILDING: {max_b}\n"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    print("\n=== CAMPUS ENERGY DASHBOARD ===\n")

    df = ingest_all_data()
    if df.empty:
        print("No data loaded. Please put CSV files inside /data/")
        return

    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    summary = building_wise_summary(df)

    create_dashboard(daily, weekly, df)
    create_outputs(df, summary)

    print("DONE. Check /output folder.")

if __name__ == "__main__":
    main()
