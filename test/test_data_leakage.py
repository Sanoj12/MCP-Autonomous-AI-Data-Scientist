import pandas as pd

from Backend.app.ml.data_leakage import detect_target_leakage


def test_target_copies_detected():

    df=pd.DataFrame({
        "age":[20,30],
        "income":[10000,23000],
        "target":[0,1],
        "target_new":[0,1]
    })

    result = detect_target_leakage(df,"target")

    assert result["leakage_detected"] is True
    assert "target_new" in result["target_copies"]




