import pandas as pd


def detect_target_leakage(
        df:pd.DataFrame,
        target_column:str,
):

    ###check target column leakage

    try:

         if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
         
         if target_column not in df.columns:

              raise ValueError(f"target column '{target_column}' not founf")


        #extract target copies

         target_copies = []

         for column in df.columns:

              if column == target_column:
                   continue

              if df[column].equals(df[target_column]):
                   target_copies.append(column)

         return {
              "target_column":target_column,
              "target_copies":target_copies,
              "leakage_detected":len(target_copies)>0

              }


    except Exception as exc:

         raise RuntimeError(f"failed to detect target column:{exc}") from exc    

        