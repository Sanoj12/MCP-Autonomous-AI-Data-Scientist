import pandas as pd

from Backend.app.ml.problem_type import detect_problem_type



def test_classification():

    df = pd.DataFrame({
        "age":[20,25,30,35],
        "churn":["yes","no","yes","no"]
    })

    result = detect_problem_type(df,"churn")

    assert result == "classification"


def test_numeric_classification():

    df = pd.DataFrame({
        "age":[20,25,30,35],
        "disease":[0,1,0,1]
    })
    result  = detect_problem_type(df,"disease")

    assert result == "classification"



def test_regression():

    df = pd.DataFrame({

        "area":[1000,1200,1500,1800],
        "price":[100000,250000,400000,550000]

    })

    result  = detect_problem_type(df,"price")

    assert result == "regression"