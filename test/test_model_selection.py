import pandas as pd
from Backend.app.ml.model_selection import model_selection

def test_model_selection():



    result = model_selection("classification")


    assert isinstance(result,dict)
    assert "logistic_regression" in result
    assert "random_forest" in result
    assert "gradient_boosting" in result
    assert "svm" in result

    