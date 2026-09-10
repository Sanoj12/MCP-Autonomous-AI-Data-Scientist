def critic(
    results: dict,
    problem_type: str,
    threshold: float
) -> dict:

    """
    Check best model performance.

    Classification:
        F1-score

    Regression:
        R2-score
    """

    try:

        if not isinstance(results, dict):
            raise ValueError("results must be a dictionary")

        if problem_type not in ["classification", "regression"]:
            raise ValueError(
                "problem_type must be 'classification' or 'regression'"
            )

        if not isinstance(threshold, (int, float)):
            raise ValueError("threshold must be a number")

        # Find best model
        best_model = None
        best_score = -1
        best_metrics = None

        model_decisions = {}

        # Check every model
        for model_name, metrics in results.items():

            if problem_type == "classification":

                if "f1_score" not in metrics:
                    raise ValueError(
                        f"f1_score missing for '{model_name}'"
                    )

                score = metrics["f1_score"]

            else:

                if "r2" not in metrics:
                    raise ValueError(
                        f"r2 missing for '{model_name}'"
                    )

                score = metrics["r2"]

            # Check model threshold
            model_acceptable = score >= threshold

            model_decisions[model_name] = {
                "score": score,
                "acceptable": model_acceptable
            }

            # Find best model
            if score > best_score:

                best_score = score
                best_model = model_name
                best_metrics = metrics

        # Final decision AFTER checking all models
        acceptable = best_score >= threshold

        if acceptable:
            action = "explain the model"
        else:
            action = "retrain the model"

        return {
            "problem_type": problem_type,
            "best_model": best_model,
            "best_score": best_score,
            "best_metrics": best_metrics,
            "threshold": threshold,
            "acceptable": acceptable,
            "action": action,
            "models": model_decisions
        }

    except Exception as exc:

        raise RuntimeError(
            f"failed model criticism: {exc}"
        ) from exc