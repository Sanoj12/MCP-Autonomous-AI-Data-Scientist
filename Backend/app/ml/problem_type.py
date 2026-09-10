import pandas as pd

def  detect_problem_type(df,target):

    try:


        if target not in df.columns:

            raise ValueError(f"Target '{target}' not found.")

        y = df[target].dropna()

        if(y.dtype == "object"
           or pd.api.types. is_bool_dtype(y)

           or #pd.api.types.is_categorical_dtype(y)
           isinstance(y.dtype, pd.CategoricalDtype)
        ):

            return "classification"


        ###numeric

        if pd.api.types.is_numeric_dtype(y):

            if y.nunique() <= 10:

                return "classification"

            return "regression"

        return "Unknown"

    except Exception as exc:

        raise RuntimeError(f"faile detect problem type:{exc}") from exc