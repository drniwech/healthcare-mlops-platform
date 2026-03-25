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
