from pathlib import Path
import pandas as pd



ALLOWED_FILE  = {".csv",".xlsx"}



def validate_file(file_path:str) -> None:
    """validate input file exists and check csv and xlsx file"""

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(f"file not found:{file_path}")

    ##check file extension eg:csv,Csv,CSV

    if path.suffix.lower() not in ALLOWED_FILE:

        raise ValueError(f"unsupported file type:{path.suffix}. only csv and xlsx files are supported.")


    return path
     

def load_file(file_path:str) -> pd.DataFrame:
    """load a csv file into pandas dataframe"""   
    try:
        path = validate_file(file_path)

    except FileNotFoundError:
        print("file not found")


    try:

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)

        elif path.suffix.lower() == ".xlsx":

            df = pd.read_excel(path)

        return df

    except FileNotFoundError as exc:

        raise FileNotFoundError(f"file not found:{path}") from exc

    
    except Exception as e:

        raise ValueError(f"unable to read file:{exc}") from exc
    
