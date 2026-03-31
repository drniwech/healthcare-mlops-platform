from kfp.v2.dsl import component, Input, Output, Metrics, Model, Dataset

@component
def evaluate_op(
    model: Input[Model],
    input_data: Input[Dataset],
    metrics: Output[Metrics],
):
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score, roc_auc_score

    df = pd.read_csv(input_data.path)

    X = df.drop(columns=["readmitted"])
    y = df["readmitted"]

    model = joblib.load(model.path)

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    acc = accuracy_score(y, preds)
    auc = roc_auc_score(y, probs)

    metrics.log_metric("accuracy", acc)
    metrics.log_metric("roc_auc", auc)
