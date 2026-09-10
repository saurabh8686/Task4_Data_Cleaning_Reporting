"""
Visualization Module

Generates and saves analytical charts.
"""

import os

import matplotlib.pyplot as plt
import seaborn as sns


def generate_charts(df, output_dir):
    """
    Generate and save project charts.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Airbnb dataset.

    output_dir : str
        Directory where charts will be saved.
    """

    os.makedirs(output_dir, exist_ok=True)

    # --------------------------------------------------
    # 1. Room Type Distribution
    # --------------------------------------------------

    plt.figure(figsize=(9, 6))

    df["room_type"].value_counts().plot(
        kind="bar"
    )

    plt.title("Airbnb Listings by Room Type")
    plt.xlabel("Room Type")
    plt.ylabel("Number of Listings")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_dir,
            "room_type_distribution.png"
        )
    )

    plt.close()

    # --------------------------------------------------
    # 2. Listings by Borough
    # --------------------------------------------------

    plt.figure(figsize=(9, 6))

    df["neighbourhood_group"].value_counts().plot(
        kind="bar"
    )

    plt.title("Airbnb Listings by Neighbourhood Group")
    plt.xlabel("Neighbourhood Group")
    plt.ylabel("Number of Listings")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_dir,
            "listings_by_borough.png"
        )
    )

    plt.close()

    # --------------------------------------------------
    # 3. Average Price by Borough
    # --------------------------------------------------

    average_price = (
        df.groupby("neighbourhood_group")["price"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 6))

    average_price.plot(
        kind="bar"
    )

    plt.title("Average Airbnb Price by Neighbourhood Group")
    plt.xlabel("Neighbourhood Group")
    plt.ylabel("Average Price")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_dir,
            "average_price_by_borough.png"
        )
    )

    plt.close()

    # --------------------------------------------------
    # 4. Price Distribution
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["price"],
        bins=50
    )

    plt.title("Airbnb Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Number of Listings")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_dir,
            "price_distribution.png"
        )
    )

    plt.close()

    print(f"✓ Charts generated in: {output_dir}")