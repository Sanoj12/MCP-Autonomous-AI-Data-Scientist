import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
import os

from Backend.app.data.loader import load_file
from Backend.app.data.data_analysis import analyze_dataset
from Backend.app.data.cleaner import clean_dataset
from Backend.app.ml.llm import llm
from Backend.app.ml.target_selector import select_target
from Backend.app.ml.problem_type import detect_problem_type
from Backend.app.ml.feature_engineering import feature_engineering
from Backend.app.ml.data_leakage import detect_target_leakage
from Backend.app.ml.data_split import split_data
from Backend.app.ml.preprocessing import create_preprocesor
from Backend.app.ml.model_selection import model_selection
from Backend.app.ml.model_trainer import train_model
from Backend.app.ml.retrain import retrain_model
from Backend.app.evaluation.metrics import (
    evaluate_classification_models,
    evaluate_regression_models
)
from Backend.app.evaluation.critic import critic

from Backend.app.mlops.mlflow_tracker import track_models
from Backend.app.mlops.model_registry import register_model
from Backend.app.artifacts.artifact import save_model_artifact
from langgraph.types import interrupt


### Load node
def load_node(state):
    df = load_file(state["file_path"])

    os.makedirs("artifacts", exist_ok=True)
    df_path = "artifacts/df.csv"
    df.to_csv(df_path, index=False)
    return {"df_path": df_path, "status": "data loaded"}


### Analysis node
def analysis_node(state):
    df = pd.read_csv(state["df_path"])
    analysis = analyze_dataset(df)
    return {"analysis": analysis, "df_path": state["df_path"]}


### Cleaning node
def cleaning_node(state):
    df = pd.read_csv(state["df_path"])
    cleaned_df, report = clean_dataset(df)
    cleaned_path = "artifacts/cleaned.csv"
    cleaned_df.to_csv(cleaned_path, index=False)
    return {"cleaned_df_path": cleaned_path, "cleaning_report": report}


### Target node
def target_node(state):
    df = pd.read_csv(state["cleaned_df_path"])
    target_column = select_target(
        llm=llm,
        objective=state["objective"],
        columns=list(df.columns)
    )
    return {"target_column": target_column}


### Problem type node
def problem_type_node(state):
    df = pd.read_csv(state["cleaned_df_path"])
    problem_type = detect_problem_type(df, state["target_column"])
    return {"problem_type": problem_type}


### Feature engineering node
def feature_node(state):
    df = pd.read_csv(state["cleaned_df_path"])
    featured_df = feature_engineering(df, state["target_column"])
    featured_path = "artifacts/featured.csv"
    featured_df.to_csv(featured_path, index=False)
    return {"featured_df_path": featured_path}


### Data leakage node
def data_leakage_node(state):
    df = pd.read_csv(state["featured_df_path"])
    leakage_report = detect_target_leakage(df, state["target_column"])
    return {"leakage_report": leakage_report}


### Train-test split node
def train_test_split_node(state):
    df = pd.read_csv(state["featured_df_path"])
    X_train, X_test, y_train, y_test = split_data(
        df, state["target_column"], state["problem_type"]
    )
    X_train.to_csv("artifacts/X_train.csv", index=False)
    X_test.to_csv("artifacts/X_test.csv", index=False)
    y_train.to_csv("artifacts/y_train.csv", index=False)
    y_test.to_csv("artifacts/y_test.csv", index=False)
    return {
        "X_train_path": "artifacts/X_train.csv",
        "X_test_path": "artifacts/X_test.csv",
        "y_train_path": "artifacts/y_train.csv",
        "y_test_path": "artifacts/y_test.csv",
        "feature_columns": X_train.columns.tolist()
    }


### Preprocessor node
def data_preprocessor_node(state):
    X_train = pd.read_csv(state["X_train_path"])
    X_test = pd.read_csv(state["X_test_path"])
    preprocessor = create_preprocesor(X_train, X_test, state["problem_type"])
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    joblib.dump(preprocessor, "artifacts/preprocessor.pkl")
    joblib.dump(X_train_processed, "artifacts/X_train_processed.pkl")
    joblib.dump(X_test_processed, "artifacts/X_test_processed.pkl")
    return {
        "X_train_processed_path": "artifacts/X_train_processed.pkl",
        "X_test_processed_path": "artifacts/X_test_processed.pkl",
        "preprocessor_path": "artifacts/preprocessor.pkl"
    }


### Model selection node
def model_selection_node(state):
    models = model_selection(state["problem_type"])
    joblib.dump(models, "artifacts/models.pkl")
    return {"models_path": "artifacts/models.pkl"}


### Model training node
def model_training_node(state):
    models = joblib.load(state["models_path"])
    X_train = joblib.load(state["X_train_processed_path"])
    y_train = pd.read_csv(state["y_train_path"])
    trained_models = train_model(models, X_train, y_train)
    joblib.dump(trained_models, "artifacts/trained_models.pkl")
    return {"trained_models_path": "artifacts/trained_models.pkl"}


### Model evaluation node
def model_evalution_node(state):
    trained_models = joblib.load(state["trained_models_path"])
    X_test = joblib.load(state["X_test_processed_path"])
    y_test = pd.read_csv(state["y_test_path"])
    if state["problem_type"] == "classification":
        results = evaluate_classification_models(trained_models, X_test, y_test)
    elif state["problem_type"] == "regression":
        results = evaluate_regression_models(trained_models, X_test, y_test)
    else:
        raise ValueError(f"unsupported problem type: {state['problem_type']}")
    return {"results": results}


### Critic node
def critic_node(state):
    critic_result = critic(state["results"], state["problem_type"], state["threshold"])
    result = {"critic_results": critic_result}
    if critic_result["acceptable"]:
        best_model_name = critic_result["best_model"]
        trained_models = joblib.load(state["trained_models_path"])
        best_model = trained_models[best_model_name]
        best_metrics = state["results"][best_model_name]
        joblib.dump(best_model, "artifacts/best_model.pkl")
        result.update({
            "best_model_name": best_model_name,
            "best_model_path": "artifacts/best_model.pkl",
            "best_metrics": best_metrics,
        })
    return result




### Retrain node
def retrain_node(state):
    X_train = joblib.load(state["X_train_processed_path"])
    X_test = joblib.load(state["X_test_processed_path"])
    y_train = pd.read_csv(state["y_train_path"])
    y_test = pd.read_csv(state["y_test_path"])
    retrain_results = retrain_model(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        problem_type=state["problem_type"],
        threshold=state["threshold"]
    )
    joblib.dump(retrain_results["trained_models"], "artifacts/retrained_models.pkl")
    return {
        "trained_models_path": "artifacts/retrained_models.pkl",
        "results": retrain_results["results"],
        "critic_results": retrain_results["critic"],
        "status": "retraining"
    }


### MLflow node
def mlflow_node(state):
    best_model = joblib.load(state["best_model_path"])
    tracking_model_result = track_models(
        model=best_model,
        model_name=state["best_model_name"],
        metrics=state["best_metrics"]
    )
    run_id = tracking_model_result
    model_uri = f"runs:/{run_id}/model"
    return {"run_id": run_id, "model_uri": model_uri}


### Registry node
def registry_node(state):
    registry_result = register_model(
        model_uri=state["model_uri"],
        model_name=state["best_model_name"]
    )
    return {"registry_result": registry_result}


### Approval node
def approval_node(state):
    approval_request = {
        "model_name": state["registry_result"]["model_name"],
        "model_version": int(state["registry_result"]["version"]),
        "metrics": state["best_metrics"],
        
    }
    decision = interrupt(approval_request)
    return {"human_approved": decision["approved"]}


def artifiacts_node(state):
    try:
        # Reload preprocessor and best model from disk
        preprocessor = joblib.load(state["preprocessor_path"])
        best_model = joblib.load(state["best_model_path"])

        # Build final pipeline
        final_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", best_model)
        ])

        # Save pipeline artifact
        artifacts_result = save_model_artifact(
            model=final_pipeline,
            output_dir="artifacts",
            file_name="model.pkl"
        )

        # Return only metadata (safe for checkpointing)
        return {
            "artifact_result": artifacts_result,
            "status": "artifact_saved"
        }

    except Exception as e:
        raise RuntimeError(f"failed artifacts node: {e}") from e
