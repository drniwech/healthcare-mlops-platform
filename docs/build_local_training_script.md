### 4. Build local training script

🎯 Objective

Build a script that:
```
- Loads features from BigQuery
- Splits train/test
- Trains model (XGBoost)
- Evaluates performance
- Saves model artifact
```

🧱 Updated Project Structure
```
training/
    train.py
    config.py
    utils.py
    model/
        (saved model will go here)
```

🧠 Why XGBoost?
- Strong baseline
- Works well on tabular healthcare data
- Easy to explain (important for healthcare trust)

🧠 What We’re Using  
```
Feature	>> Tool
Feature importance	>> XGBoost + MLflow
Confusion matrix	>> scikit-learn
Metrics JSON	>> native Python
Model versioning	>> MLflow
```

⚙️ Step 1 — Install MLflow
```ruby
</> bash
pip install mlflow matplotlib seaborn
```

🧾 Step 2 — Create training/config.py
```ruby
</> python
PROJECT_ID = "healthcare-mlops-platform"
DATASET = "healthcare_ml"
FEATURE_TABLE = "features_v2"

TARGET_COLUMN = "readmitted"

MODEL_PATH = "training/model/model.joblib"
METRICS_PATH = "training/model/metrics.json"

MLFLOW_EXPERIMENT = "healthcare-mlops"
```

🧰 Step 3 — Create training/utils.py
```ruby
</> python
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)
```

🧑‍💻 Step 4 — Create training/train.py (Production-Level)  
```ruby
</> python
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
```

▶️ Step 5 — Run Training
```ruby
</> bash
python training/train.py
```
!! Common issues:
- cannot import name 'storage' from 'google.cloud'
  - Solution:
      - pip install --upgrade google-cloud-storage
- ModuleNotFoundError: No module named 'xgboost'
  - Solution:
      - pip install xgboost
   


🔍 Expected Output

We should see logs like:
```ruby
Loading feature data from BigQuery...
Training XGBoost model...
Evaluating model...
Accuracy: 0.78
ROC-AUC: 0.84
Model saved to training/model/model.joblib
```

1️⃣ MLflow Tracking
- Experiments
- Metrics
- Artifacts
- Model registry-ready

2️⃣ Feature Importance Logging

We now:

- Explain model decisions (important for healthcare)
- Build trust (ties to the thesis 👀)

3️⃣ Confusion Matrix Artifact

Saved as:
```ruby
</> bash  
training/model/confusion_matrix.png
```

4️⃣ Metrics JSON (Pipeline-ready)
```ruby
</> JSON  
{
  "accuracy": 0.78,
  "roc_auc": 0.84
}
```
👉 This is required for:

- CI/CD pipelines
- Vertex AI pipelines

5️⃣ Model Versioning (MLflow)

Each run = new version

Later, we can:

- Register models
- Promote to production
- Rollback models

🧠 Important Insight

- Track experiments
- Store artifacts
- Version models
- Prepare for pipelines

🔥 Deliverable

We now have:
```ruby
✔ Model trained locally
✔ Evaluation metrics (AUC, accuracy)
✔ Saved model artifact
✔ Production-style training script
```
