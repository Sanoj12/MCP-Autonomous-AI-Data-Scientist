from typing import TypedDict

class DataScientistState(TypedDict, total=False):
    # =========================
    # User input
    # =========================
    file_path: str
    objective: str
    threshold: float

    # =========================
    # Data
    # =========================
    df_path: str
    analysis: dict

    cleaned_df_path: str
    cleaning_report: dict

    featured_df_path: str

    # =========================
    # ML
    # =========================
    target_column: str
    problem_type: str
    leakage_report: dict

    # Train / Test
    X_train_path: str
    X_test_path: str
    y_train_path: str
    y_test_path: str
    feature_columns: list[str]

    # Preprocessing
    X_train_processed_path: str
    X_test_processed_path: str
    preprocessor_path: str

    # =========================
    # Model
    # =========================
    models_path: str
    trained_models_path: str

    # =========================
    # Evaluation
    # =========================
    results: dict
    critic_results: dict
    best_model_name: str
    best_model_path: str
    best_metrics: dict

    

    # =========================
    # MLflow
    run_id: str
    model_uri: str
    registry_result: dict

    # =========================
    # Approval
    human_approved: bool
    feedback: str | None

    # Artifact
    artifact_result: dict

    # Status
    status: str
    message: str
