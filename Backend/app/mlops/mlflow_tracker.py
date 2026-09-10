import mlflow
import mlflow.sklearn


def track_models(
        model,
        model_name:str,
        metrics:dict,
        params:dict | None=None
):

    """track model traning using mlflow"""

    try:

        if model is None:
            raise ValueError("model cannot be none")

        if not isinstance(model_name,str):

            raise ValueError("model_name must be a string")

        if not isinstance(metrics,dict):
            raise ValueError("metrics must be dictionary")

        if params is not None and not isinstance(params,dict):

            raise ValueError("params must be a dictionary")


        ##mlflow

        with mlflow.start_run() as run:

            #model name
            mlflow.set_tag(
                "model_name",
                model_name
            )

            ##parameters

            if params:

                mlflow.log_params(params)

            mlflow.log_metrics(metrics)

            mlflow.sklearn.log_model(
                model,
                name="model"
            )

            return run.info.run_id


    except Exception as e:
        raise RuntimeError(f"failed mlflow tracking:{e}") from e
    