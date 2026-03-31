from kfp.v2.dsl import component, Output, Dataset

@component
def ingest_op(output_data: Output[Dataset]):
    from google.cloud import bigquery
    import pandas as pd

    client = bigquery.Client()

    query = """
        SELECT *
        FROM `healthcare-mlops-platform.healthcare_ml.features_v2`
    """

    df = client.query(query).to_dataframe()

    # Save to pipeline artifact path
    df.to_csv(output_data.path, index=False)
