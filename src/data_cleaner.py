"""
Data Cleaning Module

Contains reusable functions for cleaning the Airbnb dataset.
"""

import pandas as pd


def clean_data(df):
    """
    Clean the Airbnb dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw Airbnb dataset.

    Returns
    -------
    pandas.DataFrame
        Cleaned Airbnb dataset.
    """

    cleaned_df = df.copy()

    print("\n--- DATA CLEANING STARTED ---")

    # --------------------------------------------------
    # 1. Handle missing values
    # --------------------------------------------------

    cleaned_df["name"] = cleaned_df["name"].fillna(
        "Unknown Listing"
    )

    cleaned_df["host_name"] = cleaned_df["host_name"].fillna(
        "Unknown Host"
    )

    cleaned_df["reviews_per_month"] = cleaned_df[
        "reviews_per_month"
    ].fillna(0)

    # --------------------------------------------------
    # 2. Remove duplicate rows
    # --------------------------------------------------

    duplicate_rows = cleaned_df.duplicated().sum()

    cleaned_df = cleaned_df.drop_duplicates()

    print(f"✓ Duplicate rows removed: {duplicate_rows}")

    # --------------------------------------------------
    # 3. Remove duplicate listing IDs
    # --------------------------------------------------

    duplicate_ids = cleaned_df["id"].duplicated().sum()

    cleaned_df = cleaned_df.drop_duplicates(
        subset="id",
        keep="first"
    )

    print(f"✓ Duplicate IDs removed: {duplicate_ids}")

    # --------------------------------------------------
    # 4. Convert date column
    # --------------------------------------------------

    cleaned_df["last_review"] = pd.to_datetime(
        cleaned_df["last_review"],
        errors="coerce"
    )

    # --------------------------------------------------
    # 5. Convert numeric columns
    # --------------------------------------------------

    numeric_columns = [
        "id",
        "host_id",
        "latitude",
        "longitude",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365"
    ]

    for column in numeric_columns:
        cleaned_df[column] = pd.to_numeric(
            cleaned_df[column],
            errors="coerce"
        )

    # --------------------------------------------------
    # 6. Standardize text fields
    # --------------------------------------------------

    text_columns = [
        "name",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "room_type"
    ]

    for column in text_columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.strip()
        )

    # --------------------------------------------------
    # 7. Remove logically invalid records
    # --------------------------------------------------

    invalid_price = cleaned_df["price"] <= 0

    invalid_nights = cleaned_df["minimum_nights"] <= 0

    invalid_availability = (
        (cleaned_df["availability_365"] < 0) |
        (cleaned_df["availability_365"] > 365)
    )

    invalid_reviews = (
        cleaned_df["number_of_reviews"] < 0
    )

    invalid_reviews_per_month = (
        cleaned_df["reviews_per_month"] < 0
    )

    invalid_mask = (
        invalid_price |
        invalid_nights |
        invalid_availability |
        invalid_reviews |
        invalid_reviews_per_month
    )

    invalid_records = invalid_mask.sum()

    cleaned_df = cleaned_df.loc[
        ~invalid_mask
    ].copy()

    print(f"✓ Invalid records removed: {invalid_records}")

    print("\n--- DATA CLEANING COMPLETED ---")
    print(f"Final rows: {len(cleaned_df):,}")

    return cleaned_df