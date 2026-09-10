"""
Data Validation Module

Checks whether the cleaned dataset satisfies
the defined data-quality rules.
"""

import pandas as pd


def validate_data(df):
    """
    Validate the cleaned Airbnb dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned dataset.

    Returns
    -------
    dict
        Validation results.
    """

    validation_results = {
        "Duplicate Rows": df.duplicated().sum(),

        "Duplicate IDs": df["id"].duplicated().sum(),

        "Invalid Prices": (
            df["price"] <= 0
        ).sum(),

        "Invalid Minimum Nights": (
            df["minimum_nights"] <= 0
        ).sum(),

        "Invalid Availability": (
            (df["availability_365"] < 0) |
            (df["availability_365"] > 365)
        ).sum(),

        "Negative Review Counts": (
            df["number_of_reviews"] < 0
        ).sum(),

        "Negative Reviews per Month": (
            df["reviews_per_month"] < 0
        ).sum()
    }

    print("\n--- DATA VALIDATION ---")

    for check, value in validation_results.items():
        status = "PASS" if value == 0 else "CHECK"

        print(
            f"{check}: {value} → {status}"
        )

    return validation_results