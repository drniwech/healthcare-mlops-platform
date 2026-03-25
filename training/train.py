import pandas as pd
from google.cloud import bigquery
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
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

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
        joblib.dump(model, MODEL_PATH)

        mlflow.log_artifact(MODEL_PATH)
        mlflow.xgboost.log_model(model, "model")

        # --- Save JSON metrics ---
        metrics_path = save_metrics_json(acc, auc)
        mlflow.log_artifact(metrics_path)

        logger.info("Training complete with MLflow tracking")


if __name__ == "__main__":
    main()
