import pandas as pd

from Backend.app.ml.feature_engineering import feature_engineering


def test_datetime_features():

    df = pd.DataFrame({
        "age": [25, 30, 40],
        "income": [30000, 45000, 60000],
        "purchase_date": [
            "2026-01-10",
            "2026-02-15",
            "2026-08-20"
        ],
        "target": [0, 1, 1]
    })

    result = feature_engineering(
        df,
        target_column="target"
    )

    assert "purchase_date_year" in result.columns
    assert "purchase_date_month" in result.columns
    assert "purchase_date_day" in result.columns

    assert "purchase_date" not in result.columns




def test_ratio_feature():

    df = pd.DataFrame({
        "age": [25, 30, 40],
        "income": [30000, 45000, 60000],
        "target": [0, 1, 1]
    })

    result = feature_engineering(
        df,
        target_column="target"
    )

    # Check feature was created
    assert "age_per_income" in result.columns

    # Check calculation
    assert result.loc[0, "age_per_income"] == 25 / 30000

    # Target must not be used
    assert "target_per_age" not in result.columns
    assert "age_per_target" not in result.columns