## 7. Convert training into pipeline component  

🎯 Objective

Convert your training script into a Vertex AI Pipeline component so it can:

- Run reproducibly
- Be orchestrated
- Plug into full ML pipelines

🧠 What Changes Conceptually?

Before:
```
Python script → run manually
```
Now:
```
Pipeline Component → orchestrated step → reusable
```

🧱 New Structure
```
project-root/
│
├── pipeline/
│   ├── pipeline.py
│   └── components/
│       └── train_component.py
│
├── training/   (existing code stays)
```

⚙️ Step 1 — Install Pipeline SDK and virtualenv
```ruby
</> bash
 
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install kfp google-cloud-aiplatform
```
KFP = Kubeflow Pipelines (used by Vertex AI)  

🧩 Step 2 — Create Training Component  
pipeline/components/train_component.py  
```ruby
</> python  

from kfp.v2.dsl import component

@component(
    base_image="us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest"
)
def train_model_op():
    import subprocess

    # Run your existing training script inside a container
    subprocess.run(["python", "training/train.py"], check=True)
```

🧠 Why This Works

We already Dockerized your training.

👉 So instead of rewriting logic:

- We reuse our container
- Pipeline just triggers it

This is exactly how real systems are built.  

🧪 Step 3 — Create Pipeline  
pipeline/pipeline.py  
```ruby
</> python

from kfp.v2 import dsl
from kfp.v2 import compiler
from google.cloud import aiplatform

from components.train_component import train_model_op


PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"
PIPELINE_ROOT = "gs://healthcare-mlops-data/pipeline-root"
VERTEX_SERVICE_ACCOUNT = "vertex-training-sa@healthcare-mlops-platform.iam.gserviceaccount.com"

@dsl.pipeline(
    name="healthcare-mlops-pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def ml_pipeline():
    train_task = train_model_op()


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="pipeline.json"
    )

    aiplatform.init(project=PROJECT_ID, location=REGION)

    job = aiplatform.PipelineJob(
        display_name="healthcare-mlops-pipeline-run",
        template_path="pipeline.json",
        pipeline_root=PIPELINE_ROOT,
    )

    job.run(service_account=VERTEX_SERVICE_ACCOUNT)
```

🚀 Step 4 — Run Pipeline
```ruby
</> bash

python pipeline/pipeline.py
```

🔍 What Happens

Vertex AI will:

- Create pipeline job
- Pull your Docker image
- Run training step
- Log outputs

👉 We now have a managed ML pipeline.  

📊 What You’ll See in UI

Go to:

👉 Vertex AI → Pipelines

We’ll see:

- Pipeline run
- Execution graph
- Logs

✅ End of Day 7 Deliverable

We now have:
```
✔ Pipeline component
✔ Pipeline definition
✔ Pipeline execution on Vertex AI
✔ Reusable training step
```

🔥 Why This Is Huge

Before:

- One-off training job

Now:

- Reusable pipeline component
- Production orchestration
- CI/CD ready

👉 This is real MLOps architecture  

