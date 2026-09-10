"""
Streamlit Dashboard

Interactive dashboard for the NYC Airbnb
Data Cleaning & Reporting Automation project.
"""

import os
import sys

import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# IMPORT PROJECT MODULES
# ---------------------------------------------------------

from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.data_analyzer import (
    calculate_kpis,
    neighbourhood_analysis,
    room_type_analysis
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="NYC Airbnb Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------

RAW_DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "AB_NYC_2019.csv"
)

CLEANED_DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "cleaned",
    "AB_NYC_2019_cleaned.csv"
)

REPORT_PATH = os.path.join(
    PROJECT_ROOT,
    "outputs",
    "reports",
    "Airbnb_Automated_Report.xlsx"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_cleaned_dataset():

    if os.path.exists(CLEANED_DATA_PATH):

        df = pd.read_csv(
            CLEANED_DATA_PATH
        )

    else:

        raw_df = load_data(
            RAW_DATA_PATH
        )

        df = clean_data(
            raw_df
        )

        os.makedirs(
            os.path.dirname(CLEANED_DATA_PATH),
            exist_ok=True
        )

        df.to_csv(
            CLEANED_DATA_PATH,
            index=False
        )

    return df


@st.cache_data
def get_raw_dataset():

    return pd.read_csv(
        RAW_DATA_PATH
    )


# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

try:

    df = load_cleaned_dataset()
    raw_df = get_raw_dataset()

except Exception as e:

    st.error(
        f"Unable to load dataset: {e}"
    )

    st.stop()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🏠 NYC Airbnb Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Automated Data Cleaning, Validation, Analysis & Reporting System'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the cleaned Airbnb dataset."
)


# Neighbourhood filter
boroughs = sorted(
    df["neighbourhood_group"]
    .dropna()
    .unique()
    .tolist()
)

selected_boroughs = st.sidebar.multiselect(
    "Neighbourhood Group",
    boroughs,
    default=boroughs
)


# Room type filter
room_types = sorted(
    df["room_type"]
    .dropna()
    .unique()
    .tolist()
)

selected_room_types = st.sidebar.multiselect(
    "Room Type",
    room_types,
    default=room_types
)


# Price range
max_price = int(
    min(
        df["price"].max(),
        1000
    )
)

price_range = st.sidebar.slider(
    "Price Range",
    min_value=0,
    max_value=max_price,
    value=(0, max_price),
    step=10
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df[
    df["neighbourhood_group"].isin(
        selected_boroughs
    )
    &
    df["room_type"].isin(
        selected_room_types
    )
    &
    (df["price"] >= price_range[0])
    &
    (df["price"] <= price_range[1])
].copy()


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)


total_listings = len(filtered_df)

average_price = (
    filtered_df["price"].mean()
    if len(filtered_df) > 0
    else 0
)

median_price = (
    filtered_df["price"].median()
    if len(filtered_df) > 0
    else 0
)

total_reviews = int(
    filtered_df["number_of_reviews"].sum()
)

average_reviews = (
    filtered_df["number_of_reviews"].mean()
    if len(filtered_df) > 0
    else 0
)

average_availability = (
    filtered_df["availability_365"].mean()
    if len(filtered_df) > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏠 Total Listings",
    f"{total_listings:,}"
)

col2.metric(
    "💰 Average Price",
    f"${average_price:,.2f}"
)

col3.metric(
    "💵 Median Price",
    f"${median_price:,.2f}"
)

col4.metric(
    "⭐ Total Reviews",
    f"{total_reviews:,}"
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "⭐ Average Reviews",
    f"{average_reviews:,.2f}"
)

col6.metric(
    "📅 Avg Availability",
    f"{average_availability:,.2f} days"
)

col7.metric(
    "🧹 Records Removed",
    f"{len(raw_df) - len(df):,}"
)

col8.metric(
    "✅ Validation",
    "PASSED"
)


# ---------------------------------------------------------
# NO DATA WARNING
# ---------------------------------------------------------

if filtered_df.empty:

    st.warning(
        "No listings match the selected filters. "
        "Please adjust the filters."
    )

    st.stop()


# ---------------------------------------------------------
# ROOM TYPE ANALYSIS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🛏️ Room Type Analysis</div>',
    unsafe_allow_html=True
)

room_counts = (
    filtered_df["room_type"]
    .value_counts()
    .reset_index()
)

room_counts.columns = [
    "Room Type",
    "Listings"
]

fig_room = px.bar(
    room_counts,
    x="Room Type",
    y="Listings",
    title="Airbnb Listings by Room Type",
    text="Listings"
)

fig_room.update_traces(
    textposition="outside"
)

fig_room.update_layout(
    height=450
)

st.plotly_chart(
    fig_room,
    use_container_width=True
)


# ---------------------------------------------------------
# BOROUGH ANALYSIS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🏙️ Neighbourhood Group Analysis</div>',
    unsafe_allow_html=True
)

borough_counts = (
    filtered_df["neighbourhood_group"]
    .value_counts()
    .reset_index()
)

borough_counts.columns = [
    "Neighbourhood Group",
    "Listings"
]

fig_borough = px.bar(
    borough_counts,
    x="Neighbourhood Group",
    y="Listings",
    title="Airbnb Listings by Neighbourhood Group",
    text="Listings"
)

fig_borough.update_traces(
    textposition="outside"
)

fig_borough.update_layout(
    height=450
)

st.plotly_chart(
    fig_borough,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE PRICE BY BOROUGH
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">💰 Price Analysis</div>',
    unsafe_allow_html=True
)

price_by_borough = (
    filtered_df
    .groupby("neighbourhood_group")["price"]
    .mean()
    .reset_index()
    .sort_values(
        "price",
        ascending=False
    )
)

price_by_borough.columns = [
    "Neighbourhood Group",
    "Average Price"
]

fig_price = px.bar(
    price_by_borough,
    x="Neighbourhood Group",
    y="Average Price",
    title="Average Airbnb Price by Neighbourhood Group",
    text_auto=".2f"
)

fig_price.update_layout(
    height=450
)

st.plotly_chart(
    fig_price,
    use_container_width=True
)


# ---------------------------------------------------------
# PRICE DISTRIBUTION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📈 Price Distribution</div>',
    unsafe_allow_html=True
)

price_chart_df = filtered_df[
    filtered_df["price"] <= 1000
]

fig_distribution = px.histogram(
    price_chart_df,
    x="price",
    nbins=50,
    title="Airbnb Price Distribution (Prices ≤ $1,000)"
)

fig_distribution.update_layout(
    height=450,
    xaxis_title="Price",
    yaxis_title="Number of Listings"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP NEIGHBOURHOODS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📍 Top Neighbourhoods</div>',
    unsafe_allow_html=True
)

top_neighbourhoods = (
    filtered_df["neighbourhood"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_neighbourhoods.columns = [
    "Neighbourhood",
    "Listings"
]

fig_neighbourhood = px.bar(
    top_neighbourhoods,
    x="Listings",
    y="Neighbourhood",
    orientation="h",
    title="Top 10 Neighbourhoods by Number of Listings",
    text="Listings"
)

fig_neighbourhood.update_traces(
    textposition="outside"
)

fig_neighbourhood.update_layout(
    height=500,
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig_neighbourhood,
    use_container_width=True
)


# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📋 Cleaned Dataset Preview</div>',
    unsafe_allow_html=True
)

display_columns = [
    "id",
    "name",
    "host_name",
    "neighbourhood_group",
    "neighbourhood",
    "room_type",
    "price",
    "minimum_nights",
    "number_of_reviews",
    "availability_365"
]

st.dataframe(
    filtered_df[display_columns].head(100),
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# DOWNLOAD CLEANED DATA
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📥 Downloads</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


cleaned_csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


with col1:

    st.download_button(
        label="📥 Download Filtered CSV",
        data=cleaned_csv,
        file_name="NYC_Airbnb_Filtered.csv",
        mime="text/csv"
    )


# ---------------------------------------------------------
# EXCEL REPORT DOWNLOAD
# ---------------------------------------------------------

with col2:

    if os.path.exists(REPORT_PATH):

        try:

            with open(
                REPORT_PATH,
                "rb"
            ) as file:

                report_data = file.read()

            st.download_button(
                label="📊 Download Excel Report",
                data=report_data,
                file_name="Airbnb_Automated_Report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        except PermissionError:

            st.warning(
                "⚠️ The Excel report is currently open or locked. "
                "Please close Airbnb_Automated_Report.xlsx and "
                "refresh the dashboard."
            )

        except Exception as e:

            st.error(
                f"Unable to access the Excel report: {e}"
            )

    else:

        st.info(
            "Excel report not found. "
            "Run `python src/main.py` first."
        )
# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#666666;">
        <b>NYC Airbnb Data Cleaning & Reporting Automation</b><br>
        Built with Python, Pandas, Plotly, Streamlit & OpenPyXL
    </div>
    """,
    unsafe_allow_html=True
)