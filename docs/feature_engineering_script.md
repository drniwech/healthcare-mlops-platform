### Write feature engineering script  

🎯 Objective (Day 3)

Create a feature engineering script that:
```
Reads from BigQuery
Cleans & transforms data
Outputs a training-ready dataset
Can later plug into Google Vertex AI Pipelines
```

🧱 Project Structure

Inside the repo:
```
data_pipeline/
    feature_engineering.py
    config.py
    utils.py
```

🧠 What Features We Will Build

From your dataset:

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
pip install pandas google-cloud-bigquery scikit-learn
```

🧾 Step 2 — Feature Engineering Script

Create:
```
feature_engineering.py
```

```ruby
import pandas as pd
from google.cloud import bigquery


PROJECT_ID = "healthcare-mlops-platform"
DATASET = "healthcare_ml"
SOURCE_TABLE = "patient_data"
OUTPUT_TABLE = "features_v2"


def load_data():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{SOURCE_TABLE}`
    """

    df = client.query(query).to_dataframe()
    return df


def create_features(df):
    # --- Basic cleaning ---
    df = df.dropna()

    # --- Feature Engineering ---

    # Age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 50, 70, 100],
        labels=["young", "mid", "senior", "elder"]
    )

    # Medication intensity
    df["med_per_day"] = df["num_medications"] / (df["days_in_hospital"] + 1)

    # Procedure ratio
    df["procedure_ratio"] = df["num_procedures"] / (df["num_medications"] + 1)

    # High risk flag
    df["high_risk"] = (
        (df["age"] > 65) &
        (df["num_medications"] > 10)
    ).astype(int)

    # Encode categorical
    df = pd.get_dummies(df, columns=["age_group"], drop_first=True)

    return df


def save_to_bigquery(df):
    client = bigquery.Client(project=PROJECT_ID)

    table_id = f"{PROJECT_ID}.{DATASET}.{OUTPUT_TABLE}"

    job = client.load_table_from_dataframe(df, table_id)
    job.result()

    print(f"Saved features to {table_id}")


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
