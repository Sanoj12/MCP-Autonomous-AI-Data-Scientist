import pandas as pd


def train_model(
        models: dict,
        X_train,
        y_train
) -> dict:

    """Train selected machine learning models."""

    try:

        if not isinstance(models, dict):
            raise ValueError("models must be a dictionary")

        if X_train is None:
            raise ValueError("X_train cannot be None")

        if y_train is None:
            raise ValueError("y_train cannot be None")

        trained_models = {}

        for model_name, model in models.items():

            if model is None:
                raise ValueError(
                    f"model '{model_name}' cannot be None"
                )

            model.fit(X_train, y_train)

            trained_models[model_name] = model

        return trained_models

    except Exception as exc:
        raise RuntimeError( f"failed model training:{exc}") from exc