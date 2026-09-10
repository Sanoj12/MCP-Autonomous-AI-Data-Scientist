import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,RobustScaler

def create_preprocesor( X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    problem_type: str
):
    """create preprocessing pipeline"""

    try:

         if not isinstance(X_train,pd.DataFrame):

            raise TypeError("X_train must be a pandas dataframe.")

         if not isinstance(X_test,pd.DataFrame):
         
                     raise TypeError("X_test must be a pandas dataframe.")


         #Find numeric columns

         numeric_columns = X_train.select_dtypes(include=["number"]).columns.to_list()

         #find categorical columns

         categorical_columns = X_train.select_dtypes(
            include=["object","category","bool"]
         ).columns.to_list()


         numerical_pipeline= Pipeline(
               steps=[
                     #fill missing vlaues
                     (
                           "imputer",
                           SimpleImputer(strategy="median")
                     ),
                     (
                           "scaler",
                           RobustScaler()
                     )
               ]
         )


         categorical_pipeline = Pipeline(
               steps=[
                     (
                           "imputer",
                           SimpleImputer(strategy="most_frequent")
                     ),
                     (
                           "scaler",
                           OneHotEncoder(handle_unknown="ignore")
                     )
               ]
         )



         ##combine transformation

         preprocessor  = ColumnTransformer(
            transformers= [
               (
                  "numeric",
                  numerical_pipeline,
                  numeric_columns,
                 
               ),
               (
                  "categorical",
                  categorical_pipeline,
                  categorical_columns,
                  
               )
            ]
         )

         return preprocessor


    except Exception as e:

        raise RuntimeError(f"failed getting durning preprocessing:{e}") from e
    