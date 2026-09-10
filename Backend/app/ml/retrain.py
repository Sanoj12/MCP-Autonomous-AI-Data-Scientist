import pandas as pd

from Backend.app.ml.model_selection import model_selection
from Backend.app.ml.model_trainer import train_model
from Backend.app.evaluation.metrics import evaluate_classification_models,evaluate_regression_models
from Backend.app.evaluation.critic import critic

def retrain_model(
    X_train,
    X_test,
    y_train,
    y_test,
    problem_type: str,
  
    threshold: float = 0.80
) -> dict:

    try:

        # 1. Select models again
        models = model_selection(problem_type)

        # 2. Train models
        trained_models = train_model(
            models,
            X_train,
            y_train
        )

        # 3. Evaluate again
        if problem_type == "classification":

            results = evaluate_classification_models(
                trained_models,
                X_test,
                y_test
            )

        else:

            results = evaluate_regression_models(
                trained_models,
                X_test,
                y_test
            )

        # 4. Critic checks new results
        critic_result = critic(
            results,
            problem_type,
            threshold
        )

        # 5. Return new result
        return {
            "status": "retrained",
            "results": results,
            "critic": critic_result,
            "trained_models": trained_models
        }

    except Exception as exc:

        raise RuntimeError(
            f"Retraining failed: {exc}"
        ) from exc

