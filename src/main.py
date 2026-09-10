"""
Main Automation Pipeline

Runs the complete NYC Airbnb data cleaning,
validation, analysis, visualization, and
reporting workflow.
"""

import os

from data_loader import load_data
from data_cleaner import clean_data
from data_validator import validate_data
from data_analyzer import (
    calculate_kpis,
    neighbourhood_analysis,
    room_type_analysis
)
from visualization import generate_charts
from report_generator import generate_report


# ==========================================================
# PROJECT PATHS
# ==========================================================

RAW_DATA_PATH = "data/raw/AB_NYC_2019.csv"

CLEANED_DATA_PATH = (
    "data/cleaned/AB_NYC_2019_cleaned.csv"
)

CHARTS_PATH = "outputs/charts"

REPORT_PATH = (
    "outputs/reports/Airbnb_Automated_Report.xlsx"
)


# ==========================================================
# MAIN PIPELINE
# ==========================================================

def main():

    print("=" * 60)
    print(" NYC AIRBNB DATA CLEANING & REPORTING AUTOMATION")
    print("=" * 60)

    # ------------------------------------------------------
    # STEP 1 — LOAD DATA
    # ------------------------------------------------------

    print("\n[1/7] Loading raw dataset...")

    df = load_data(RAW_DATA_PATH)

    # ------------------------------------------------------
    # STEP 2 — BEFORE CLEANING METRICS
    # ------------------------------------------------------

    print("\n[2/7] Creating pre-cleaning quality baseline...")

    before_metrics = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum(),
        "Duplicate IDs": df["id"].duplicated().sum(),
        "Zero Prices": (df["price"] == 0).sum(),
        "Negative Prices": (df["price"] < 0).sum(),
        "Invalid Minimum Nights": (
            df["minimum_nights"] <= 0
        ).sum(),
        "Invalid Availability": (
            (df["availability_365"] < 0) |
            (df["availability_365"] > 365)
        ).sum(),
        "Negative Review Counts": (
            df["number_of_reviews"] < 0
        ).sum()
    }

    # ------------------------------------------------------
    # STEP 3 — CLEAN DATA
    # ------------------------------------------------------

    print("\n[3/7] Cleaning dataset...")

    cleaned_df = clean_data(df)

    # ------------------------------------------------------
    # STEP 4 — VALIDATE DATA
    # ------------------------------------------------------

    print("\n[4/7] Validating cleaned dataset...")

    validation_results = validate_data(cleaned_df)

    # ------------------------------------------------------
    # STEP 5 — ANALYSIS
    # ------------------------------------------------------

    print("\n[5/7] Calculating analytical results...")

    kpis = calculate_kpis(cleaned_df)

    neighbourhood_data = neighbourhood_analysis(
        cleaned_df
    )

    room_type_data = room_type_analysis(
        cleaned_df
    )

    print("\n--- KEY PERFORMANCE INDICATORS ---")

    for key, value in kpis.items():
        print(f"{key}: {value}")

    # ------------------------------------------------------
    # STEP 6 — GENERATE CHARTS
    # ------------------------------------------------------

    print("\n[6/7] Generating visualizations...")

    generate_charts(
        cleaned_df,
        CHARTS_PATH
    )

    # ------------------------------------------------------
    # STEP 7 — AFTER METRICS & REPORT
    # ------------------------------------------------------

    print("\n[7/7] Generating final report...")

    after_metrics = {
        "Rows": len(cleaned_df),
        "Columns": len(cleaned_df.columns),
        "Missing Values": cleaned_df.isnull().sum().sum(),
        "Duplicate Rows": cleaned_df.duplicated().sum(),
        "Duplicate IDs": cleaned_df["id"].duplicated().sum(),
        "Zero Prices": (cleaned_df["price"] == 0).sum(),
        "Negative Prices": (cleaned_df["price"] < 0).sum(),
        "Invalid Minimum Nights": (
            cleaned_df["minimum_nights"] <= 0
        ).sum(),
        "Invalid Availability": (
            (cleaned_df["availability_365"] < 0) |
            (cleaned_df["availability_365"] > 365)
        ).sum(),
        "Negative Review Counts": (
            cleaned_df["number_of_reviews"] < 0
        ).sum()
    }

    # ------------------------------------------------------
    # SAVE CLEANED DATA
    # ------------------------------------------------------

    os.makedirs(
        os.path.dirname(CLEANED_DATA_PATH),
        exist_ok=True
    )

    cleaned_df.to_csv(
        CLEANED_DATA_PATH,
        index=False
    )

    print(
        f"\n✓ Cleaned dataset saved to: "
        f"{CLEANED_DATA_PATH}"
    )

    # ------------------------------------------------------
    # GENERATE EXCEL REPORT
    # ------------------------------------------------------

    generate_report(
        output_path=REPORT_PATH,
        before_metrics=before_metrics,
        after_metrics=after_metrics,
        validation_results=validation_results,
        kpis=kpis,
        neighbourhood_data=neighbourhood_data,
        room_type_data=room_type_data
    )

    # ------------------------------------------------------
    # FINAL SUMMARY
    # ------------------------------------------------------

    print("\n" + "=" * 60)
    print(" PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nOriginal records : {len(df):,}")
    print(f"Cleaned records  : {len(cleaned_df):,}")
    print(
        f"Records removed  : "
        f"{len(df) - len(cleaned_df):,}"
    )

    print("\nGenerated outputs:")
    print(f"✓ {CLEANED_DATA_PATH}")
    print(f"✓ {CHARTS_PATH}/")
    print(f"✓ {REPORT_PATH}")

    print("\nAutomation completed successfully! 🎉")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()