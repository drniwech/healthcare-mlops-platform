### 3. Write feature engineering script  

🎯 Objective 

Create a feature engineering script that:
```
- Reads from BigQuery
- Cleans & transforms data
- Outputs a training-ready dataset
- Can later plug into Google Vertex AI Pipelines
```

🧱 Project Structure

Inside the repo:
```
data_pipeline/
    feature_engineering.py
    config.py
    utils.py
```

We separate concerns:
```
config.py → environment/config values
utils.py → reusable helpers (logging, validation, etc.)
```
This makes our code:
```
- cleaner
- reusable
- pipeline-ready (for Google Vertex AI later)
```

🧠 What Features We Will Build

From our dataset:

Input Columns:
- age
- num_procedures
- num_medications
- days_in_hospital

Add NEW Features:  
Feature	>> Why  
age_group	>> better model signal  
med_per_day	>> intensity of treatment  
procedure_ratio	>> complexity  
high_risk_flag	>> domain-based feature    

🧑‍💻 Step 1 — Install Dependencies
```ruby
</> bash
pip install pandas google-cloud-bigquery scikit-learn db-dtypes
```

!!! If your pip install for pandas or google-cloud-bigquery is stuck on "Running setup.py", run the following command:  
```
pip install --upgrade pip setuptools wheel
```
🧾 Step 2 — Feature Engineering Script

🧾 1. Create config.py
```ruby
</> python
# data_pipeline/config.py

PROJECT_ID = "healthcare-mlops-platform"
DATASET = "healthcare_ml"

SOURCE_TABLE = "patient_data"
OUTPUT_TABLE = "features_v2"

LOCATION = "US"
```
👉 Later, we can replace this with env variables (production best practice).  

🧰 2. Create utils.py

Start simple but useful.
```ruby
</> python
# data_pipeline/utils.py

import logging


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def validate_dataframe(df):
    if df.empty:
        raise ValueError("DataFrame is empty")

    if df.isnull().sum().sum() > 0:
        print("Warning: Data contains null values")

    return True
```

Create:
```
feature_engineering.py
```

```ruby
import pandas as pd
from google.cloud import bigquery

from config import PROJECT_ID, DATASET, SOURCE_TABLE, OUTPUT_TABLE
from utils import setup_logger, validate_dataframe

logger = setup_logger()


def load_data():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{SOURCE_TABLE}`
    """

    logger.info("Loading data from BigQuery...")
    df = client.query(query).to_dataframe()

    validate_dataframe(df)
    return df


def create_features(df):
    logger.info("Creating features...")

    df = df.dropna()

    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 50, 70, 100],
        labels=["young", "mid", "senior", "elder"]
    )

    df["med_per_day"] = df["num_medications"] / (df["days_in_hospital"] + 1)
    df["procedure_ratio"] = df["num_procedures"] / (df["num_medications"] + 1)

    df["high_risk"] = (
        (df["age"] > 65) &
        (df["num_medications"] > 10)
    ).astype(int)

    df = pd.get_dummies(df, columns=["age_group"], drop_first=True)

    return df


def save_to_bigquery(df):
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET}.{OUTPUT_TABLE}"

    logger.info(f"Saving features to {table_id}...")
    job = client.load_table_from_dataframe(df, table_id)
    job.result()

    logger.info("Save complete!")


def main():
    df = load_data()
    df_features = create_features(df)
    save_to_bigquery(df_features)


if __name__ == "__main__":
    main()
```

▶️ Step 3 — Run It
```ruby
</> bash
python data_pipeline/feature_engineering.py
```

🔍 Step 4 — Validate in BigQuery

Run:
```ruby
</> SQL
SELECT *
FROM healthcare_ml.features_v2
LIMIT 10;
```  
Check:

- New columns exist
- No weird values
- No null explosion

### Deliverable

We now have:
```
✔ Automated feature pipeline
✔ New feature table (features_v2)
✔ Reusable script (not notebook)
✔ Ready for training step
```
