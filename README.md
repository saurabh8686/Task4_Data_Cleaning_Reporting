# 🏠 Automated Data Cleaning & Reporting System for NYC Airbnb Listings

<p align="center">

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge&logo=streamlit)](https://task4datacleaningreporting-kuuujxplybdsyaidvuqejw.streamlit.app/)

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/atharva123-buddy/Task4_Data_Cleaning_Reporting)

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)

[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?style=for-the-badge&logo=pandas)](https://pandas.pydata.org/)

[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

</p>

## 🚀 Live Demo

**Interactive Streamlit Dashboard:**  
https://task4datacleaningreporting-kuuujxplybdsyaidvuqejw.streamlit.app/

**GitHub Repository:**  
https://github.com/atharva123-buddy/Task4_Data_Cleaning_Reporting

---

## 📌 Project Overview

This project implements an end-to-end **Data Cleaning, Validation, Analysis, Visualization, and Automated Reporting System** using the **NYC Airbnb Open Data** dataset.

The system converts raw Airbnb listing data into a validated and analysis-ready dataset, generates analytical visualizations, creates a professionally formatted Excel report, and provides an interactive Streamlit dashboard for exploration.

The project is designed as an internship-level data analytics automation solution demonstrating practical skills in:

- Data ingestion
- Data profiling
- Data cleaning
- Missing-value handling
- Duplicate detection
- Data validation
- Outlier analysis
- Exploratory data analysis
- Data visualization
- Excel report automation
- Interactive dashboard development
- Python modular programming
- Git/GitHub version control
- Streamlit deployment

---

## 🎯 Project Objectives

The main objectives are to:

1. Load and inspect a raw real-world dataset.
2. Profile the dataset and identify data-quality issues.
3. Clean missing, duplicate, inconsistent, and invalid records.
4. Validate the cleaned dataset using predefined quality rules.
5. Calculate important business KPIs.
6. Analyze listings by neighbourhood group and room type.
7. Generate automated charts.
8. Create a professional Excel analytics report.
9. Build an interactive Streamlit dashboard.
10. Provide downloadable cleaned data and reports.
11. Create a reusable Python automation pipeline.
12. Deploy the dashboard for public access.

---

# 🔄 End-to-End Workflow

```text
Raw Airbnb CSV
      ↓
Data Ingestion
      ↓
Data Profiling
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
Clean Dataset
      ↓
Data Analysis
      ↓
Visualization
      ↓
Automated Excel Report
      ↓
Streamlit Interactive Dashboard
      ↓
Final Outputs
```

---

# 📊 Dataset

## Dataset Used

**NYC Airbnb Open Data**

Source: Kaggle  
https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data

The dataset contains Airbnb listings in New York City.

### Dataset Dimensions

| Metric | Value |
|---|---:|
| Original Rows | 48,895 |
| Columns | 16 |
| Cleaned Rows | 48,884 |
| Records Removed | 11 |

### Dataset Columns

| Column | Description |
|---|---|
| `id` | Unique Airbnb listing ID |
| `name` | Listing name |
| `host_id` | Host identifier |
| `host_name` | Host name |
| `neighbourhood_group` | NYC borough |
| `neighbourhood` | Specific neighbourhood |
| `latitude` | Listing latitude |
| `longitude` | Listing longitude |
| `room_type` | Type of accommodation |
| `price` | Price per night |
| `minimum_nights` | Minimum number of nights |
| `number_of_reviews` | Total number of reviews |
| `last_review` | Date of latest review |
| `reviews_per_month` | Average reviews per month |
| `calculated_host_listings_count` | Number of listings owned by host |
| `availability_365` | Availability during the year |

---

# 🔎 Phase 1 — Data Profiling

The profiling stage examines the raw dataset before any cleaning is performed.

### Profiling Tasks

- Dataset dimensions
- Column names
- Data types
- Dataset preview
- Random sample inspection
- Statistical summary
- Missing-value analysis
- Duplicate-row detection
- Duplicate-ID detection
- Categorical-value analysis
- Numerical validation
- Price outlier analysis
- Pre-cleaning quality baseline

### Notebook

```text
notebooks/01_data_profiling.ipynb
```

The profiling notebook intentionally focuses on **understanding the data rather than modifying it**.

---

# 🧹 Phase 2 — Data Cleaning

The cleaning pipeline is implemented as reusable Python functions.

## Missing-Value Handling

The project uses business-aware missing-value handling rather than blindly deleting missing records.

| Column | Treatment |
|---|---|
| `name` | Filled with `Unknown Listing` |
| `host_name` | Filled with `Unknown Host` |
| `reviews_per_month` | Filled with `0` |
| `last_review` | Missing values retained |

`last_review` is intentionally not filled because a missing review date can legitimately indicate that a listing has no recorded review.

## Duplicate Handling

The pipeline checks and removes:

- Complete duplicate rows
- Duplicate listing IDs

## Data-Type Standardization

The pipeline converts:

- Date fields to datetime
- Numeric fields to numeric data types
- Text fields to standardized string values
- Leading/trailing whitespace is removed

## Invalid-Record Removal

The following logical validation rules are applied:

- `price > 0`
- `minimum_nights > 0`
- `availability_365` must be between `0` and `365`
- `number_of_reviews >= 0`
- `reviews_per_month >= 0`

## Outlier Handling

Price outliers are identified using the **IQR method**.

Outliers are **not automatically deleted** because extreme Airbnb prices can represent legitimate listings. The project separates data-quality errors from valid but unusual observations.

### Cleaning Notebook

```text
notebooks/02_data_cleaning.ipynb
```

---

# 📈 Cleaning Results

The automated pipeline produced the following result:

| Metric | Before | After |
|---|---:|---:|
| Records | 48,895 | 48,884 |
| Columns | 16 | 16 |
| Records Removed | — | 11 |
| Duplicate Rows | 0 | 0 |
| Duplicate IDs | 0 | 0 |
| Invalid Prices | — | 0 |
| Invalid Minimum Nights | — | 0 |
| Invalid Availability | — | 0 |

The cleaned dataset is saved as:

```text
data/cleaned/AB_NYC_2019_cleaned.csv
```

---

# ✅ Phase 3 — Data Validation

After cleaning, the dataset is passed through a separate validation module.

### Validation Checks

- Duplicate rows
- Duplicate IDs
- Invalid prices
- Invalid minimum nights
- Invalid availability
- Negative review counts
- Negative reviews per month

### Final Validation

All defined validation rules passed successfully.

```text
Duplicate Rows: 0 → PASS
Duplicate IDs: 0 → PASS
Invalid Prices: 0 → PASS
Invalid Minimum Nights: 0 → PASS
Invalid Availability: 0 → PASS
Negative Review Counts: 0 → PASS
Negative Reviews per Month: 0 → PASS
```

Validation is separated from cleaning so that the final dataset can be independently checked after transformation.

---

# 📊 Phase 4 — Data Analysis

The analysis module calculates business KPIs and grouped analytical summaries.

## Key Performance Indicators

| KPI | Result |
|---|---:|
| Total Listings | 48,884 |
| Average Price | $152.76 |
| Median Price | $106.00 |
| Total Reviews | 1,137,628 |
| Average Reviews | 23.27 |
| Average Availability | 112.78 days |
| Average Minimum Nights | 7.03 nights |

> Prices are reported in the dataset's original currency/unit representation.

## Neighbourhood-Group Analysis

The system calculates:

- Number of listings
- Average price
- Average reviews
- Average availability

for each NYC neighbourhood group.

## Room-Type Analysis

The system calculates:

- Number of listings
- Average price
- Average reviews

for each room type.

---

# 📉 Phase 5 — Data Visualization

The project automatically generates four main charts:

### 1. Room Type Distribution

Shows the distribution of Airbnb listings across room types.

```text
outputs/charts/room_type_distribution.png
```

### 2. Listings by Borough

Shows the number of listings across NYC neighbourhood groups.

```text
outputs/charts/listings_by_borough.png
```

### 3. Average Price by Borough

Compares average listing prices between neighbourhood groups.

```text
outputs/charts/average_price_by_borough.png
```

### 4. Price Distribution

Displays the distribution of listing prices.

```text
outputs/charts/price_distribution.png
```

The visualization module uses Matplotlib and Seaborn.

---

# 📑 Phase 6 — Automated Excel Reporting

The system automatically creates a professionally formatted Excel workbook:

```text
outputs/reports/Airbnb_Automated_Report.xlsx
```

## Workbook Structure

### 1. Dashboard

Contains:

- Project title
- KPI cards
- Four analytical charts
- Executive summary

### 2. Data Quality

Contains:

- Before-cleaning metrics
- After-cleaning metrics
- Records removed
- Quality comparison

### 3. Validation

Contains all validation checks and PASS/CHECK status.

### 4. Neighbourhood Analysis

Contains neighbourhood-group analytical results.

### 5. Room Type Analysis

Contains room-type analytical results.

### Report Features

- Professional formatting
- Styled headers
- KPI section
- Embedded charts
- Number formatting
- Borders
- Automatic column widths
- Frozen panes
- Executive summary

---

# 🖥️ Phase 7 — Streamlit Interactive Dashboard

The project also includes a live Streamlit dashboard.

## Dashboard Features

### Interactive Filters

Users can filter listings by:

- Neighbourhood group
- Room type
- Price range

### KPI Cards

The dashboard displays:

- Total Listings
- Average Price
- Median Price
- Total Reviews
- Average Reviews
- Average Availability
- Records Removed
- Validation Status

### Interactive Visualizations

The dashboard includes:

- Room type distribution
- Listings by borough
- Average price by borough
- Price distribution
- Top 10 neighbourhoods

### Data Preview

Users can inspect the filtered cleaned dataset directly in the dashboard.

### Downloads

The dashboard provides downloadable:

- Filtered CSV data
- Automated Excel report

---

# 🏗️ Project Architecture

```text
Task4_Data_Cleaning_Reporting/
│
├── data/
│   ├── raw/
│   │   └── AB_NYC_2019.csv
│   │
│   └── cleaned/
│       └── AB_NYC_2019_cleaned.csv
│
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   └── 02_data_cleaning.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── data_validator.py
│   ├── data_analyzer.py
│   ├── visualization.py
│   ├── report_generator.py
│   └── main.py
│
├── outputs/
│   ├── charts/
│   └── reports/
│
├── reports/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧩 Python Modules

| Module | Responsibility |
|---|---|
| `data_loader.py` | Loads raw CSV data |
| `data_cleaner.py` | Cleans and standardizes data |
| `data_validator.py` | Validates cleaned data |
| `data_analyzer.py` | Calculates KPIs and grouped analysis |
| `visualization.py` | Generates charts |
| `report_generator.py` | Creates Excel report |
| `main.py` | Runs complete automation pipeline |
| `app.py` | Runs interactive Streamlit dashboard |

This modular architecture makes the project easier to maintain, test, reuse, and extend.

---

# 🛠️ Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **OpenPyXL**
- **Plotly**
- **Streamlit**
- **Jupyter Notebook**
- **Git**
- **GitHub**
- **Kaggle Dataset**

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/atharva123-buddy/Task4_Data_Cleaning_Reporting.git
cd Task4_Data_Cleaning_Reporting
```

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# ▶️ Run the Automated Pipeline

From the project root:

```powershell
python src/main.py
```

The pipeline automatically:

1. Loads the raw dataset
2. Creates a pre-cleaning baseline
3. Cleans the data
4. Validates the cleaned data
5. Calculates KPIs
6. Generates analytical summaries
7. Creates charts
8. Saves the cleaned CSV
9. Generates the Excel report
10. Prints the final execution summary

---

# 🌐 Run Streamlit Locally

From the project root:

```powershell
streamlit run app.py
```

The dashboard will open in your browser.

---

# 📦 Generated Outputs

After running the pipeline:

```text
data/cleaned/
└── AB_NYC_2019_cleaned.csv

outputs/charts/
├── room_type_distribution.png
├── listings_by_borough.png
├── average_price_by_borough.png
└── price_distribution.png

outputs/reports/
└── Airbnb_Automated_Report.xlsx
```

---

# 🧪 Testing

The automation pipeline was tested successfully.

Expected execution summary:

```text
Original records : 48,895
Cleaned records  : 48,884
Records removed  : 11

Duplicate Rows: 0 → PASS
Duplicate IDs: 0 → PASS
Invalid Prices: 0 → PASS
Invalid Minimum Nights: 0 → PASS
Invalid Availability: 0 → PASS
Negative Review Counts: 0 → PASS
Negative Reviews per Month: 0 → PASS
```

The complete pipeline finishes successfully and generates all expected outputs.

---

# 💡 Key Business Insights

The project demonstrates how automated data processing can support Airbnb marketplace analysis.

Examples of insights available through the system include:

- Distribution of listings across NYC boroughs
- Differences in average prices between neighbourhood groups
- Relative popularity of room types
- Review activity across listings
- Availability patterns
- Neighbourhood-level listing concentration
- Price distribution and extreme-value behaviour

The dashboard allows these patterns to be explored interactively rather than relying only on static reports.

---

# 🧠 Data Quality Philosophy

The project follows a practical data-quality approach:

### 1. Profile Before Cleaning

The raw data is examined before transformations are applied.

### 2. Business-Aware Cleaning

Missing values are handled according to their meaning rather than automatically deleting rows.

### 3. Separate Cleaning and Validation

Cleaning changes the dataset; validation verifies that the resulting dataset satisfies defined rules.

### 4. Do Not Blindly Delete Outliers

Unusual values are investigated instead of automatically assuming they are errors.

### 5. Reproducible Automation

The same Python pipeline can be rerun whenever new data becomes available.

---

# 🔐 `.gitignore`

The project excludes unnecessary environment and Python-generated files:

```text
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
```

This keeps the GitHub repository clean and avoids committing local virtual-environment files.

---

# ☁️ Streamlit Deployment

The Streamlit dashboard has been deployed using **Streamlit Community Cloud**.

### Live Application

https://task4datacleaningreporting-kuuujxplybdsyaidvuqejw.streamlit.app/

The application is connected to the GitHub repository and uses the project's `requirements.txt` for dependencies.

For deployment, the application entry point is:

```text
app.py
```

and dependencies are defined in:

```text
requirements.txt
```

---

# 📸 Screenshots / Portfolio Presentation

For a stronger GitHub portfolio presentation, screenshots can be added to a future `screenshots/` directory:

```text
screenshots/
├── streamlit_dashboard.png
├── excel_dashboard.png
└── github_repository.png
```

They can then be displayed in this README using:

```markdown
![Streamlit Dashboard](screenshots/streamlit_dashboard.png)

![Excel Dashboard](screenshots/excel_dashboard.png)
```

This is recommended because screenshots give recruiters and reviewers an immediate visual understanding of the project.

---

# 🔮 Future Enhancements

Possible improvements include:

- Automated scheduled data refresh
- Database integration
- Power BI dashboard
- Advanced anomaly detection
- Automated email reports
- Cloud-based data storage
- Historical trend analysis
- Machine-learning-based price prediction
- Geographic/map-based visualization
- Automated data-quality alerts
- Unit tests for individual modules
- CI/CD using GitHub Actions
- Docker deployment

---

# ⚠️ Limitations

- The analysis is based on the provided NYC Airbnb dataset.
- The dataset represents a historical snapshot rather than live Airbnb inventory.
- Price outliers are retained when they are not demonstrably invalid.
- The project does not establish causal relationships between variables.
- Results depend on the quality and completeness of the source dataset.
- The dashboard is primarily designed for exploratory analytics rather than production-scale data warehousing.

---

# 🎓 Learning Outcomes

This project demonstrates practical understanding of:

- Python for data analytics
- Pandas data manipulation
- NumPy numerical operations
- Data profiling
- Data cleaning
- Missing-value treatment
- Duplicate detection
- Data validation
- Outlier analysis
- Exploratory data analysis
- Matplotlib and Seaborn visualization
- Plotly interactive visualization
- Excel automation using OpenPyXL
- Streamlit dashboard development
- Modular Python programming
- File and folder organization
- Git and GitHub
- Cloud deployment
- End-to-end analytics automation

---

# 💼 Internship Task

**Task:** Data Cleaning & Reporting Automation

### Expected Skills

- Python / Excel / Power BI
- Data preprocessing
- Missing-value handling
- Duplicate removal
- Inconsistent-data handling
- Automated reporting
- Visual summaries

### Expected Outcome

Understand data preprocessing, automation, reporting efficiency, and data-driven visualization through a complete real-world project.

---

# 👨‍💻 Author

## Atharva Joshi

**GitHub:**  
https://github.com/atharva123-buddy

**Project Repository:**  
https://github.com/atharva123-buddy/Task4_Data_Cleaning_Reporting

---

# 📌 Final Project Summary

This project provides a complete automated workflow for transforming raw NYC Airbnb data into a clean, validated, analyzed, visualized, and report-ready dataset.

It combines:

```text
Python Automation
        +
Data Cleaning
        +
Data Validation
        +
Data Analysis
        +
Visualization
        +
Excel Reporting
        +
Interactive Streamlit Dashboard
        +
GitHub Version Control
        +
Cloud Deployment
```

The result is a reusable analytics system that reduces manual data-cleaning and reporting effort while providing both static Excel reporting and an interactive web-based dashboard.

---

# 🔗 Quick Links

| Resource | Link |
|---|---|
| 🚀 Live Dashboard | https://task4datacleaningreporting-kuuujxplybdsyaidvuqejw.streamlit.app/ |
| 💻 GitHub Repository | https://github.com/atharva123-buddy/Task4_Data_Cleaning_Reporting |
| 📊 Kaggle Dataset | https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data |
| 🐍 Python | https://www.python.org/ |
| 📈 Pandas | https://pandas.pydata.org/ |
| 📊 Streamlit | https://streamlit.io/ |

---

<p align="center">

### ⭐ If you find this project useful, consider giving the repository a star!

**Built with Python, Pandas, Streamlit, OpenPyXL, Matplotlib, Seaborn & Plotly**

</p>