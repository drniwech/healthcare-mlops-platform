import pandas as pd
import json


def build_features(raw_input):
    # -------------------------
    # Step 1: Base features
    # -------------------------
    data = {
        "age": raw_input["age"],
        "num_procedures": raw_input["num_procedures"],
        "num_medications": raw_input["num_medications"],
        "days_in_hospital": raw_input["days_in_hospital"],
        "med_per_day": raw_input["num_medications"]
        / (raw_input["days_in_hospital"] + 1),
        "procedure_ratio": raw_input["num_procedures"]
        / (raw_input["num_medications"] + 1),
        "high_risk": int(raw_input["age"] > 65 and raw_input["num_medications"] > 10),
        # Add categorical fields (IMPORTANT)
        "gender": raw_input.get("gender"),
        "diagnosis": raw_input.get("diagnosis"),
    }

    df = pd.DataFrame([data])

    # -------------------------
    # Step 2: One-hot encoding
    # -------------------------
    df = pd.get_dummies(df)

    # -------------------------
    # Step 3: Align with training schema
    # -------------------------
    with open("training/artifacts/feature_columns.json") as f:
        training_cols = json.load(f)

    # Enables:
    # - Safe deployment
    # - Drift detection
    # - Retraining
    df = df.reindex(columns=training_cols, fill_value=0)

    return df
