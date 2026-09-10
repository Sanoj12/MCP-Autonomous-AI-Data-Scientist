import pytest

from Backend.app.data.data_analysis import analyze_dataset
from Backend.app.data.loader import load_file


def test_dataset_analysis():

    # Load your actual CSV
    df = load_file("C:/Users/sanoj/MCP-Autonomous-AI-Data-Scientist/data/telecom_churn.csv")

    # Analyze the dataset
    result = analyze_dataset(df)

    # Basic checks
    assert not df.empty

    assert isinstance(result, dict)

    # Check key 
    assert "shape" in result
    assert "column_types" in result
    assert "missing_values" in result
    assert "duplicate_rows" in result
    assert "cardinality" in result
    assert "numeric_summary" in result