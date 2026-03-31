## Convert training into pipeline component  

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

⚙️ Step 1 — Install Pipeline SDK
```ruby
</> bash
 
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
