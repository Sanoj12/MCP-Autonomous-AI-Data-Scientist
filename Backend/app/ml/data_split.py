from sklearn.model_selection import train_test_split


def split_data(df, target_column, problem_type):

    try:


        X = df.drop(columns=[target_column])
        
        y = df[target_column].squeeze()

        if problem_type == "classification":

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y
            )

        elif problem_type == "regression":

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

        else:

            raise ValueError(
                f"Unsupported problem type: {problem_type}"
            )

        return X_train, X_test, y_train, y_test

    except Exception as e:

        raise RuntimeError(
            f"failed to getting train test split: {e}"
        ) from e