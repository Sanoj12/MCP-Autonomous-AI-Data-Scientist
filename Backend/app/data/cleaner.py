import pandas as pd
import numpy as np



def clean_dataset(df:pd.DataFrame):

    """clean the dataset """

    try:

        if not isinstance(df,pd.DataFrame):

          raise TypeError("input must be a pandas daataframe")


        cleaned_df = df.copy()


        report = {
           "rows":len(cleaned_df),
           "columns":len(cleaned_df.columns),
           "missing_values":int(cleaned_df.isna().sum().sum()),
           "duplicates_values":int(cleaned_df.duplicated().sum()),
           "explanation":[]
        }

        
        ##remove completely empty rows###################3
        removed = int(cleaned_df.isna().all(axis=1).sum())

        cleaned_df = cleaned_df.dropna(
           how="all"
        )

        if removed>0:
           report["explanation"].append(f"Removed {removed} completely empty rows.")



        ### Remove duplicate rows######################

        duplicates = cleaned_df.duplicated().sum()

        if duplicates > 0:

           cleaned_df = cleaned_df.drop_duplicates()

           report["explanation"].append(f"Removed {duplicates} duplicate rows")


        ###clean column names #######3

        old_columns = cleaned_df.columns.to_list()

        cleaned_df.columns=(
           cleaned_df.columns
           .str.strip()
           .str.lower()
           .str.replace(" ","_")
           .str.replace(r"[^\w]+", "_", regex=True)
           .str.strip("_")
        )

        ##check with old columns

        if old_columns != cleaned_df.columns.tolist():

           report["explanation"].append("Standardized column names.")



        ######Handle missing values##############

        
        for column in cleaned_df.columns:

           missing = cleaned_df[column].isna().sum()

           if missing == 0:
              continue

           ###numeric - median

           if pd.api.types.is_numeric_dtype(cleaned_df[column]):

              median_value = cleaned_df[column].median()


              cleaned_df[column]=(
                 cleaned_df[column].fillna(median_value)
              )


              report["explanation"].append(
                 f"filled {missing} missing values"
                 f" in '{column}' with median."
              )

           ### categorical -> mode
           else:

              mode = cleaned_df[column].mode()

              if not mode.empty:

                 #first actual mode
                 mode_value = mode.iloc[0]
                
                 cleaned_df[column]=(
                   
                   cleaned_df[column].fillna(mode_value)

                 )


                 report["explanation"].append(
                   f"filled {missing} missing values"
                   f" in '{column}' with mode."
                 )


              else:

                 cleaned_df[column]=(
                    cleaned_df[column].fillna("Unknown")
                 )


                 report["explanation"].append(
                    f"filled missing values in"
                    f" '{column}' with 'Unknown'"
                 )

        #### FINAL REPORT

        report["final_rows"] = len(cleaned_df)

        report["final_columns"] = len(
           cleaned_df.columns
        )

        report["missing_values_after"] = int(
           cleaned_df.isna().sum().sum()
        )

        report["duplicates_after"] = int(
           cleaned_df.duplicated().sum()
        )


        report["rows_removed"] =(
           report["rows"] - report["final_rows"]
        )


        return cleaned_df,report

    except Exception as exc:

       raise RuntimeError(f"failed to data cleaning:{exc}") from exc