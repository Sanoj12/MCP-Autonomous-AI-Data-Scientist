import shap
import pandas as pd

def explain_model(model, X_train, X_test, feature_names=None) -> dict:
    """Generate SHAP explanation for the trained model."""

    if model is None:
        raise ValueError("model cannot be None")
    if X_train is None:
        raise ValueError("X_train cannot be None")
    if X_test is None:
        raise ValueError("X_test cannot be None")

    # Create SHAP explainer
    explainer = shap.Explainer(model, X_train)

    # Calculate SHAP values
    shap_values = explainer(X_test)

    # If arrays, use provided feature_names or fallback to indices
    if feature_names is None:
        if isinstance(X_train, pd.DataFrame):
            feature_names = X_train.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]

    # Summarize SHAP values into serializable form
    shap_summary = shap_values.values.mean(axis=0).tolist()

    return {
        "feature_names": feature_names,
        "shap_summary": shap_summary
    }
