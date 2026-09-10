import pytest
import pandas as pd
from Backend.app.data.loader import load_file

from Backend.app.data.data_analysis import analyze_dataset

from Backend.app.data.cleaner import clean_dataset


def test_data_cleaner():

    df = load_file("C:/Users/sanoj/MCP-Autonomous-AI-Data-Scientist/data/telecom_churn.csv")

    #
    cleaned_df,report = clean_dataset(df)

    ##check returntype
    assert isinstance(cleaned_df , pd.DataFrame)
    assert isinstance(report,dict)


    ##check report
    assert "rows" in report
    assert "final_rows" in report

    assert "columns" in report
    assert "final_columns" in report

    assert "missing_values" in report
    assert "missing_values_after" in report

    assert "duplicates_values" in report
    assert "duplicates_after" in report

    assert "rows_removed" in report
    assert "explanation" in report



