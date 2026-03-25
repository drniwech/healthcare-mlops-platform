### Build local training script

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
