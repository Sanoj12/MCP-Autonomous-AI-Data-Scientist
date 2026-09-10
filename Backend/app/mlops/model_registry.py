import mlflow

def register_model(
        model_uri:str,
        model_name:str
) -> dict:

     """Register a trained model in MLflow Model Registry."""

     try:

          if not isinstance(model_uri,str):

               raise ValueError("model_uri must be string")

          if not isinstance(model_name,str):

               raise ValueError("model_name must be a string")



          if not model_uri:
               raise ValueError("model uri cannot empty")

          if not model_name:
               raise ValueError("model name cannot empty")


          registered_model = mlflow.register_model(
               model_uri = model_uri,
               name = model_name
          )

          return{
               "model_name":registered_model.name,
               "version":registered_model.version
          }

     except Exception as e:

          raise RuntimeError(f"failed model registration:{e}") from e