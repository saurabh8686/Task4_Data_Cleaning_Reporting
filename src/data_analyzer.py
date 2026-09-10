"""
Data Analysis Module

Calculates business KPIs and analytical summaries
from the cleaned Airbnb dataset.
"""

import pandas as pd


def calculate_kpis(df):
    """
    Calculate key performance indicators.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Airbnb dataset.

    Returns
    -------
    dict
        KPI values.
    """

    kpis = {
        "Total Listings": len(df),

        "Average Price": round(
            df["price"].mean(), 2
        ),

        "Median Price": round(
            df["price"].median(), 2
        ),

        "Total Reviews": int(
            df["number_of_reviews"].sum()
        ),

        "Average Reviews": round(
            df["number_of_reviews"].mean(), 2
        ),

        "Average Availability": round(
            df["availability_365"].mean(), 2
        ),

        "Average Minimum Nights": round(
            df["minimum_nights"].mean(), 2
        )
    }

    return kpis


def neighbourhood_analysis(df):
    """
    Generate neighbourhood-group level analysis.
    """

    result = (
        df.groupby("neighbourhood_group")
        .agg(
            Listings=("id", "count"),
            Average_Price=("price", "mean"),
            Average_Reviews=("number_of_reviews", "mean"),
            Average_Availability=("availability_365", "mean")
        )
        .round(2)
        .sort_values(
            "Listings",
            ascending=False
        )
    )

    return result


def room_type_analysis(df):
    """
    Generate room-type analysis.
    """

    result = (
        df.groupby("room_type")
        .agg(
            Listings=("id", "count"),
            Average_Price=("price", "mean"),
            Average_Reviews=("number_of_reviews", "mean")
        )
        .round(2)
        .sort_values(
            "Listings",
            ascending=False
        )
    )

    return result