import pandas as pd
from google.cloud import bigquery, storage
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix
from xgboost import XGBClassifier
import joblib
import os
import json
import mlflow
import mlflow.xgboost
import matplotlib.pyplot as plt
import seaborn as sns

from config import *
from utils import setup_logger

logger = setup_logger()


def load_data():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{FEATURE_TABLE}`
    """

    df = client.query(query).to_dataframe()
    return df


def prepare_data(df):
    # Separate features and target
    X = df.drop(columns=[TARGET_COLUMN])
    # df[TARGET_COLUMN] dtype: Int64 (Pandas nullable type)
    # preds dtype: int64 (NumPy standard int) 
    # The problem is: Int64 (capital I) ≠ int64
    y = df[TARGET_COLUMN].astype(int)  # We fix it here.

    # -------------------------
    # Handle categorical columns. Encode categorical features.
    # -------------------------
    categorical_cols = ["gender", "diagnosis"]

    # pd.get_dummies() is a pandas function used to convert categorical variables into "dummy" or indicator variables, 
    # a process commonly known as one-hot encoding. It transforms each unique value in a column into its own new column 
    # containing binary values (1 or 0, or True/False).
    X = pd.get_dummies(X, columns=categorical_cols)

    # -------------------------
    # Save feature columns 
    # -------------------------
    os.makedirs("training/artifacts", exist_ok=True)
    feature_path = "training/artifacts/feature_columns.json"

    # Saves our training feature schema
    with open(feature_path, "w") as f:
        json.dump(list(X.columns), f)

    logger.info(f"Saved feature columns to {feature_path}")

    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(X_train, y_train):
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    return model


def plot_confusion_matrix(y_test, preds):
    cm = confusion_matrix(y_test, preds)

    plt.figure()
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Confusion Matrix")

    os.makedirs("training/model", exist_ok=True)
    path = "training/model/confusion_matrix.png"
    plt.savefig(path)
    plt.close()

    return path


def save_metrics_json(acc, auc):
    metrics = {
        "accuracy": acc,
        "roc_auc": auc
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    return METRICS_PATH

def upload_to_gcs(local_path, gcs_path):
    client = storage.Client()

    bucket_name = gcs_path.split("/")[2]
    blob_path = "/".join(gcs_path.split("/")[3:])

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    blob.upload_from_filename(local_path)

    print(f"Uploaded model to {gcs_path}")

def main():
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    with mlflow.start_run():

        df = load_data()
        X_train, X_test, y_train, y_test = prepare_data(df)

        model = train_model(X_train, y_train)

        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, preds)
        auc = roc_auc_score(y_test, probs)

        # --- Log metrics ---
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("roc_auc", auc)

        logger.info(f"Accuracy: {acc:.4f}")
        logger.info(f"AUC: {auc:.4f}")

        # --- Feature importance ---
        importances = model.feature_importances_
        for i, col in enumerate(X_train.columns):
            mlflow.log_metric(f"importance_{col}", float(importances[i]))

        # --- Confusion matrix ---
        cm_path = plot_confusion_matrix(y_test, preds)
        mlflow.log_artifact(cm_path)

        # --- Save model ---
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        # Save locally
        joblib.dump(model, MODEL_PATH)

        # Upload to GCS (NEW)
        upload_to_gcs(MODEL_PATH, MODEL_GCS_PATH)

        # MLflow logging
        mlflow.log_artifact(MODEL_PATH)
        mlflow.xgboost.log_model(model, "model")

        # --- Save JSON metrics ---
        metrics_path = save_metrics_json(acc, auc)
        mlflow.log_artifact(metrics_path)

        logger.info("Training complete with MLflow tracking")


if __name__ == "__main__":
    main()
