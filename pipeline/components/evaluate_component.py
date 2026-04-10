from kfp.v2.dsl import component, Input, Output, Metrics, Model, Dataset


@component
def evaluate_op(
    model: Input[Model],
    input_data: Input[Dataset],
    metrics: Output[Metrics],
):
    import pandas as pd
    import joblib
    import json
    from sklearn.metrics import accuracy_score, roc_auc_score

    # -------------------------
    # Load data
    # -------------------------
    df = pd.read_csv(input_data.path)

    # -------------------------
    # Separate features & target
    # -------------------------
    X = df.drop(columns=["readmitted"])
    # FIX dtype mismatch between int (primitive) and Int (Pandas nullable
    # type).
    y = df["readmitted"].astype(int)

    # -------------------------
    # Apply the same encoding as training
    # pd.get_dummies() is a pandas function used to convert categorical variables into "dummy" or indicator variables,
    # a process commonly known as one-hot encoding. It transforms each unique value in a column into its own new column
    # containing binary values (1 or 0, or True/False).
    # -------------------------
    X = pd.get_dummies(X)

    # -------------------------
    # Align with training schema
    # -------------------------
    with open("training/artifacts/feature_columns.json") as f:
        training_cols = json.load(f)

    # Adds missing columns
    # Removes extra columns
    # Orders columns exactly like training
    # fill_value=0? In one-hot encoding: 0 = category not present
    X = X.reindex(columns=training_cols, fill_value=0)

    # -------------------------
    # Load model
    # -------------------------
    model = joblib.load(model.path)

    # -------------------------
    # Predictions
    # -------------------------
    # FIX dtype mismatch between int (primitive) and Int (Pandas nullable
    # type).
    preds = model.predict(X).astype(int)
    probs = model.predict_proba(X)[:, 1].astype(float)

    # -------------------------
    # Metrics
    # -------------------------
    acc = accuracy_score(y, preds)
    auc = roc_auc_score(y, probs)

    metrics.log_metric("accuracy", acc)
    metrics.log_metric("roc_auc", auc)
