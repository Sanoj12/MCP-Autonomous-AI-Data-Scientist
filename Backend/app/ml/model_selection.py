import pandas as pd

from sklearn.linear_model import LogisticRegression,LinearRegression

from sklearn.svm import SVC,SVR


from sklearn.ensemble import (
    RandomForestClassifier,RandomForestRegressor,
    GradientBoostingClassifier,GradientBoostingRegressor
)



def model_selection(problem_type:str):
    """select different model"""

    try:

        if problem_type == "classification":

            return{
                "logistic_regression":LogisticRegression(
                    max_iter =100,
                
                ),
                "svm":SVC(),
                "random_forest":RandomForestClassifier(
                    n_estimators=200,
                    random_state=42
                ),
                "gradient_boosting":GradientBoostingClassifier(
                    random_state=42
                )


            }

        elif problem_type == "regression":
            return{
                "linear_regression":LinearRegression(),

                "random_forest":RandomForestRegressor(
                    n_estimators=200,
                    random_state=42
                ),
                "gradient_boosting":GradientBoostingRegressor(
                    random_state=42
                ),
                "svr":SVR()
            }

        else:

            raise ValueError("Problem_type must be 'classification' or 'regression'")


    except Exception as exc:
        raise RuntimeError(f"failed model selection:{exc}") from exc    