import pandas as pd


def load_data(file_path):
    """Load marketing data from CSV."""
    df = pd.read_csv(file_path)
    return df


def clean_data(df):
    """Clean and prepare marketing data."""

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows where customer ID is missing
    df = df.dropna(subset=["customer_id"])

    # Find numerical columns
    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    # Fill missing numerical values
    for column in numeric_columns:
        df[column] = df[column].fillna(
            df[column].median()
        )

    # Find text columns
    text_columns = df.select_dtypes(
        include=["object"]
    ).columns

    # Fill missing text values
    for column in text_columns:
        df[column] = df[column].fillna(
            "Unknown"
        )

    return df