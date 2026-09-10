import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,recall_score,f1_score,
    mean_absolute_error,mean_squared_error,r2_score
)



def evaluate_classification_models(
        trained_models:dict,
        X_test,
        y_test,
) ->dict:

    """evalaute trained classification models"""

    try:

        if not isinstance(trained_models,dict):

            raise ValueError("trained_models must be a dictionary")

        if X_test is None: 

             raise ValueError( "X_test cannot be None" )

        if y_test is None: 
        
             raise ValueError( "y_test cannot be None" )
        
         


        results={}

        for model_name,model in trained_models.items():

            predictions = model.predict(X_test)

            results[model_name] = {
                "accuracy":accuracy_score(
                    y_test,predictions
                ),
                "precision":precision_score(
                    y_test,predictions,average="weighted"
                ),

                "recall":recall_score(
                    y_test,predictions,average="weighted"
                ),

                "f1_score": f1_score(
                    y_test,predictions,average="weighted"
                )
            } 

        return results
    except Exception as exc:

        raise RuntimeError(f"failed evaluation classification models:{exc}") from exc




def evaluate_regression_models(
        trained_models: dict,
        X_test,
        y_test
) -> dict:

    """evalaute trained regression models"""

    try:

        if not isinstance(trained_models, dict):
            raise ValueError( "trained_models must be a dictionary" ) 

        if X_test is None: 
         
            raise ValueError( "X_test cannot be None" )
         
        if y_test is None: 
                 
            raise ValueError( "y_test cannot be None" )




        results={}


        for model_name,model in trained_models.items():

            predictions = model.predict(X_test)

            mse = mean_squared_error(
                    y_test,
                    predictions
                )

            results[model_name] ={
                "mse": mse,

                "mae":mean_absolute_error(
                    y_test,predictions
                ),

                "rmse":mse ** 0.5,

                "r2": r2_score(
                    y_test,predictions
                )
            
            }
        return results

    except Exception as e:

        raise RuntimeError(f"failed evalaution regression models:{e}") from e
