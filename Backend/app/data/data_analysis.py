import pandas as pd


##data analysis
import pandas as pd


def get_column_types(df: pd.DataFrame) -> dict:

    """check numeric, categorical, datetime, and other columns."""
    try:
        ##check the type of particular value

        if not isinstance(df, pd.DataFrame):

            raise TypeError("input must be a pandas DataFrame.")

        numeric_columns = df.select_dtypes( include=["number"]).columns.tolist()


        categorical_columns = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


        datetime_columns = df.select_dtypes(include=["datetime"]).columns.tolist()

        return {
            "numeric": numeric_columns,
            "categorical": categorical_columns,
            "datetime": datetime_columns,
        }

    except Exception as exc:

        raise RuntimeError(f"failed to get column types: {exc}") from exc


def check_missing_values(df: pd.DataFrame) -> dict:

    """Return missing value statistics."""
    try:
        if not isinstance(df, pd.DataFrame):

            raise TypeError("Input must be a pandas DataFrame.")

        missing = df.isnull().sum()
        results = {}

        for column, count in missing.items():
            if count > 0:
                results[column] = {
                    "count": int(count),
                    "percentage": round((count / len(df)) * 100, 2)
                }

        return results

    except Exception as exc:
        raise RuntimeError(f"Failed to check missing values: {exc}") from exc


def get_duplicate_count(df: pd.DataFrame) -> int:

    """Return number of duplicate rows."""
    try:

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")


        return int(df.duplicated().sum())

    except Exception as e:

        raise RuntimeError(f"Failed to check duplicates: {e}") from e



###3check statistic summary of numeric columns-mean,median,std

def get_numeric_summary(df:pd.DataFrame) -> dict:

    """generate descriptive statistics for numeric columns"""

    try:

        if not isinstance(df, pd.DataFrame):

            raise TypeError("Input must be a pandas DataFrame.")

        
        numeric_df = df.select_dtypes(include=["number"])

        return numeric_df.describe().round(3).to_dict()

    except Exception as exc:

          raise RuntimeError(f"failed to get statistic summary :{exc}") from exc        
    


##check unique value for row

def check_cardianlity(df:pd.DataFrame) ->dict:

    """return number of unique values for every column"""

    try:

        if not isinstance(df,pd.DataFrame):

            raise TypeError("Input must be a pandas DataFrame.")

        return {
           column: int(df[column].nunique(dropna=True))
           for column in df.columns
        }

    except Exception as exc:

        raise RuntimeError(f"failed to check unique value")


#combine all individual analysis into dataset report

def analyze_dataset(df:pd.DataFrame) -> dict:

    """generate complete dataset"""

    try:

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        return{
            "shape":{
                "rows":int(df.shape[0]),
                "columns":int(df.shape[1])
            },
            "column_types":get_column_types(df),
            "missing_values":check_missing_values(df),
            "duplicate_rows":get_duplicate_count(df),
            "cardinality":check_cardianlity(df),
            "numeric_summary":get_numeric_summary(df)
        }

    except Exception as exc:

        raise RuntimeError(f"failed to analyze dataset:{exc}") from exc