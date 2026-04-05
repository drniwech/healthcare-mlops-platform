# domain-specific config
PROJECT_ID = "healthcare-mlops-platform"
DATASET = "healthcare_ml"
FEATURE_TABLE = "features_v2"

TARGET_COLUMN = "readmitted"

# Local paths
MODEL_PATH = "training/model/model.joblib"
METRICS_PATH = "training/model/metrics.json"

# Cloud paths (NEW)
BUCKET_NAME = "healthcare-mlops-data"
MODEL_GCS_PATH = f"gs://{BUCKET_NAME}/models/model.joblib"

# MLflow
MLFLOW_EXPERIMENT = "healthcare-mlops"
