#!/usr/bin/env python3
"""
ETL Pipeline generated from Jupyter notebooks.
"""
import os
import pathlib
import warnings
import numpy as np
import pandas as pd
import re

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)

def load_raw_file(directory: pathlib.Path) -> pd.DataFrame:
    """Auto-detect and load the first supported file in the given directory."""
    supported = {
        ".csv":  lambda p: pd.read_csv(p, low_memory=False),
        ".xlsx": lambda p: pd.read_excel(p),
        ".xls":  lambda p: pd.read_excel(p),
        ".json": lambda p: pd.read_json(p),
    }

    for filepath in sorted(directory.iterdir()):
        ext = filepath.suffix.lower()
        if ext in supported and not filepath.name.startswith("."):
            print(f"Detected file : {filepath.name}")
            print(f"Format        : {ext.upper().lstrip('.')}")
            df = supported[ext](filepath)
            print(f"Loaded        : {len(df):,} rows x {len(df.columns)} columns")
            return df

    raise FileNotFoundError(f"No supported file found in {directory}")

def iqr_bounds(series: pd.Series, factor: float = 1.5):
    """Return (lower, upper) Winsorization bounds using the IQR method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - factor * iqr, q3 + factor * iqr

def classify_brain_rot(index_value):
    """Map a brain_rot_index value to its corresponding level label."""
    if pd.isna(index_value):
        return np.nan
    if index_value <= 15:
        return "Low"
    elif index_value <= 30:
        return "Medium"
    else:
        return "High"

def run_etl():
    print('Starting ETL Pipeline...')

    # --- 1. Extraction ---
    RANDOM_STATE = 42
    SAMPLE_SIZE  = 100_000
    
    # Paths
    # Assuming scripts/ is the current dir or one level below root
    # Using pathlib for robust path resolution
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    RAW_DIR = base_dir / "data" / "raw"
    PROCESSED_DIR = base_dir / "data" / "processed"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH = PROCESSED_DIR / "cleaned_data.csv"
    
    print(f"Raw data directory : {RAW_DIR}")
    
    df_raw = load_raw_file(RAW_DIR)

    total_rows = len(df_raw)
    
    if total_rows > SAMPLE_SIZE:
        df = df_raw.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE).reset_index(drop=True)
        print(f"Sampled {SAMPLE_SIZE} rows from {total_rows}")
    else:
        df = df_raw.copy().reset_index(drop=True)
        print(f"Using all {total_rows} rows.")
    
    if "student_id" in df.columns:
        df["student_id"] = range(1, len(df) + 1)

    # --- 2. Cleaning ---
    # Normalize column names
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(r"[^a-z0-9]+", "_", regex=True)
          .str.strip("_")
    )
    
    # Drop columns >70% nulls
    high_null_cols = df.columns[df.isnull().mean() > 0.70].tolist()
    if high_null_cols:
        df.drop(columns=high_null_cols, inplace=True)
    
    # Sentinel strings
    NULL_SENTINELS = ["", "NA", "N/A", "na", "n/a", "not applicable",
                      "Not Applicable", "NULL", "null", "-", "."]
    
    obj_cols = df.select_dtypes(include="object").columns
    df[obj_cols] = df[obj_cols].replace(NULL_SENTINELS, np.nan)
    
    for col in obj_cols:
        df[col] = df[col].str.strip() if df[col].dtype == object else df[col]
    
    # Impute numeric columns with median
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    
    for col in num_cols:
        if col == "student_id":
            continue
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    
    # Impute categorical columns with mode
    for col in cat_cols:
        if col == "brain_rot_level":
            continue
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
    
    # Winsorize numeric columns
    measure_cols = [c for c in num_cols if c != "student_id"]
    for col in measure_cols:
        lower, upper = iqr_bounds(df[col])
        df[col] = df[col].clip(lower=lower, upper=upper)
    
    # Re-check object columns after sentinel replacement
    obj_cols_now = [c for c in df.select_dtypes(include="object").columns if c != "brain_rot_level"]
    for col in obj_cols_now:
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.notna().mean() > 0.90:
            df[col] = converted
    
    # Binary encoding
    BINARY_MAP = {"yes": 1, "no": 0, "true": 1, "false": 0, "y": 1, "n": 0}
    obj_cols_now = df.select_dtypes(include="object").columns
    for col in obj_cols_now:
        unique_vals = df[col].dropna().astype(str).str.lower().unique()
        if set(unique_vals).issubset(BINARY_MAP.keys()):
            df[col] = df[col].astype(str).str.lower().map(BINARY_MAP)
    
    # Rederive brain_rot_level
    if "brain_rot_index" in df.columns:
        df["brain_rot_level"] = df["brain_rot_index"].apply(classify_brain_rot)
    
    # Engineer academic_risk_score
    required_cols = ["class_attendance_rate", "academic_motivation", "digital_addiction_score", "brain_rot_index"]
    if all(c in df.columns for c in required_cols):
        df["academic_risk_score"] = (
            (100 - df["class_attendance_rate"]) * 0.4 +
            (10 - df["academic_motivation"]) * 2.5 +
            df["digital_addiction_score"] * 0.5 +
            df["brain_rot_index"] * 0.3
        )
        df["academic_risk_score"] = df["academic_risk_score"].clip(lower=0)
    
    # Round float columns
    float_cols = df.select_dtypes(include="float").columns
    df[float_cols] = df[float_cols].round(2)
    
    # --- 3. Final Prep & Load ---
    # Validation checks
    df.drop_duplicates(inplace=True)
    
    print(f"Final shape: {df.shape}")
    print(f"Total nulls remaining: {df.isnull().sum().sum()}")
    
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_etl()
