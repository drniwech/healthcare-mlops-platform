## Build full pipeline: Ingest → Train → Evaluate → Register  

🧱 Final Pipeline Structure  
```
pipeline/
├── pipeline.py
└── components/
    ├── ingest_component.py
    ├── train_component.py
    ├── evaluate_component.py
    └── register_component.py
```

⚙️ Step 1 — Ingest Component  
pipeline/components/ingest_component.py  
```ruby
</> python

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

```

⚙️ Step 2 — Train Component  
pipeline/components/train_component.py  
```ruby
</> python

from kfp.v2.dsl import component, Input, Output, Model, Dataset

@component
def train_op(
    input_data: Input[Dataset],
    model_output: Output[Model],
):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from xgboost import XGBClassifier
    import joblib

    df = pd.read_csv(input_data.path)

    X = df.drop(columns=["readmitted"])
    y = df["readmitted"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, model_output.path)
```

⚙️ Step 3 — Evaluate Component  
pipeline/components/evaluate_component.py  
```ruby
</> python

from kfp.v2.dsl import component, Input, Output, Metrics, Model, Dataset

@component
def evaluate_op(
    model: Input[Model],
    input_data: Input[Dataset],
    metrics: Output[Metrics],
):
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score, roc_auc_score

    df = pd.read_csv(input_data.path)

    X = df.drop(columns=["readmitted"])
    y = df["readmitted"]

    model = joblib.load(model.path)

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    acc = accuracy_score(y, preds)
    auc = roc_auc_score(y, probs)

    metrics.log_metric("accuracy", acc)
    metrics.log_metric("roc_auc", auc)
```

⚙️ Step 4 — Register Model Component  
pipeline/components/register_component.py  
```ruby
</> python

from kfp.v2.dsl import component, Input, Model

@component
def register_model_op(model: Input[Model]):
    from google.cloud import aiplatform

    aiplatform.init(
        project="healthcare-mlops-platform",
        location="us-central1"
    )

    aiplatform.Model.upload(
        display_name="healthcare-readmission-model",
        artifact_uri=model.path,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-5:latest",
    )
```

🧩 Step 5 — Build Full Pipeline  
pipeline/pipeline.py  
```ruby
</> python

from kfp.v2 import dsl, compiler
from google.cloud import aiplatform

from components.ingest_component import ingest_op
from components.train_component import train_op
from components.evaluate_component import evaluate_op
from components.register_component import register_model_op

PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"
PIPELINE_ROOT = "gs://healthcare-mlops-data/pipeline-root"


@dsl.pipeline(
    name="healthcare-full-mlops-pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def ml_pipeline():

    ingest_task = ingest_op()

    train_task = train_op(
        input_data=ingest_task.outputs["output_data"]
    )

    eval_task = evaluate_op(
        model=train_task.outputs["model_output"],
        input_data=ingest_task.outputs["output_data"]
    )

    register_task = register_model_op(
        model=train_task.outputs["model_output"]
    )


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="pipeline.json"
    )

    aiplatform.init(project=PROJECT_ID, location=REGION)

    job = aiplatform.PipelineJob(
        display_name="healthcare-full-pipeline-run",
        template_path="pipeline.json",
        pipeline_root=PIPELINE_ROOT,
    )

    job.run()
```

🚀 Step 6 — Run Pipeline  
```ruby
</> bash

python pipeline/pipeline.py
```

🔍 What Happens Now

Vertex AI executes:
```
1. Ingest data from BigQuery
2. Train model
3. Evaluate model
4. Register model
```

✅ Final Deliverable 
```
✔ End-to-end ML pipeline
✔ Automated training + evaluation
✔ Model registry integration
✔ Reproducible workflows
```

We:

- Built a full pipeline
- Added orchestration
- Connected to model registry

👉 This is real enterprise MLOps
