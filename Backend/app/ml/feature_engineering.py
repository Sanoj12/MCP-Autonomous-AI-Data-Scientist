# ml/feature_engineering.py

import pandas as pd
import numpy as np


def detect_datetime_columns(df):
    """Detect columns containing datetime values."""

    date_columns = []

    for column in df.columns:

        # already datetime

        if pd.api.types.is_datetime64_any_dtype(df[column]):
            date_columns.append(column)
            continue

        # only check object/string columns
        
        if df[column].dtype not in ["object", "string"]:
            continue

        converted = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        # Consider it datetime if 70%+ values convert
        if converted.notna().mean() >= 0.70:
            date_columns.append(column)

    return date_columns


def create_datetime_features(df, date_columns):

    """Convert datetime columns into numeric features."""

    df = df.copy()

    for column in date_columns:

        date = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        df[f"{column}_year"] = date.dt.year

        df[f"{column}_month"] = date.dt.month

        df[f"{column}_day"] = date.dt.day
        df[f"{column}_weekday"] = date.dt.dayofweek
        df[f"{column}_is_weekend"] = (
            date.dt.dayofweek >= 5
        ).astype(int)

        # Remove original datetime column
        df.drop(
            columns=column,
            inplace=True
        )

    return df


def create_ratio_features(df, target_column):
    """Create ratio features between multiple numeric columns."""

    df = df.copy()

    numeric_columns = [
        column
        for column in df.select_dtypes(
            include=np.number
        ).columns
        if column != target_column
    ]

    # Example: age, income, expenses  eg:income_per_age
    for i in range(len(numeric_columns)):

        for j in range(i + 1, len(numeric_columns)):

            col1 = numeric_columns[i]
            col2 = numeric_columns[j]

            # Avoid division by zero
            denominator = df[col2].replace(
                0,
                np.nan
            )

            feature_name = (
                f"{col1}_per_{col2}"
            )

            ##
            df[feature_name] = (
                df[col1] / denominator
            )

    # Remove infinity
    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return df


def feature_engineering(df, target_column):
    """Main feature engineering function."""

    df = df.copy()

    
    #Detect datetime


    date_columns = detect_datetime_columns(df)

    #  Create datetime features
    

    df = create_datetime_features(
        df,
        date_columns
    )

    
    #Create numeric ratios
  

    df = create_ratio_features(
        df,
        target_column
    )

    return df