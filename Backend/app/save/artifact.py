import os 
import joblib

def save_model_artifact(
        model,
        output_dir:str="artifacts",
        file_name:str ="model.pkl",
) -> dict:

    """save the approved ml model as a pickle file"""

    try:

        if model is None:
            raise ValueError("model cannot be None")


        if not isinstance(output_dir,str):

            raise ValueError("output_direcionary must be a string")

        if not isinstance(file_name,str):

            raise ValueError("file name must be a string")

        if not file_name.endswith(".pkl"):

            raise ValueError("file name must have .pkl extension.")

        ###create directionary

        os.makedirs(output_dir,exist_ok=True)

        ## create file 
        file_path = os.path.join(output_dir,file_name)


        ##save model
        joblib.dump(model,file_path)

        return{
            "status":"success",
            "file_path":file_path,
            "file_name":file_name,
            "message":"model  file created successfully"        
        }

    except Exception as e:

        raise RuntimeError(f"failed to create model artifact:{e}") from e