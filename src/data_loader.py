"""
Data Loader Module

Responsible for loading raw datasets into pandas DataFrames.
"""

import pandas as pd


def load_data(file_path):
    """
    Load a CSV dataset.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    try:
        df = pd.read_csv(file_path)

        print("✓ Dataset loaded successfully")
        print(f"  Rows: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")

        return df

    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        raise

    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        raise