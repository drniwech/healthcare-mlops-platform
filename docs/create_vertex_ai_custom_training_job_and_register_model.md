## Create Vertex AI custom training job and register model  

🎯 Objective
- Push Docker image → Artifact Registry
- Run Vertex AI Custom Training Job
- Register trained model in Model Registry

🧠 Architecture We’re Implementing
```
Local → Docker → Artifact Registry → Vertex AI Training → Model Registry
```  
This is exactly what companies do.  

⚙️ Step 1 — Create Artifact Registry Repo
```ruby
</> bash

gcloud artifacts repositories create mlops-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="MLOps Docker repo"
```

🔐 Step 2 — Authenticate Docker
```ruby
</> bash

gcloud auth configure-docker us-central1-docker.pkg.dev
```

🏗 Step 3 — Tag Docker Image
```ruby
</> bash

docker tag healthcare-mlops:latest \
us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest
```

🚀 Step 4 — Push Image
```ruby
</> bash

docker push \
us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest
```

🧪 Step 5 — Run Vertex AI Custom Training Job
```ruby
</> bash

gcloud ai custom-jobs create \
--region=us-central1 \
--display-name=healthcare-training-job \
--worker-pool-spec=machine-type=e2-standard-4,replica-count=1,container-image-uri=us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest
```

🔍 What Happens Now

Vertex AI will:

- Pull our Docker image
- Run our training script
- Execute MLflow logging
- Produce model artifact  

👉 We just ran serverless ML training  

⚠️ IMPORTANT (Model Artifact Location)

Right now, our model is saved locally inside the container:
```ruby
</> bash

training/model/model.joblib
```

👉 This will be LOST after the job finishes.  

✅ Fix — Save Model to Cloud Storage

Update our config.py:
```ruby
</> python

MODEL_GCS_PATH = "gs://healthcare-mlops-data/models/model.joblib"
```

Update save logic:  
```ruby
</> python

from google.cloud import storage

def upload_to_gcs(local_path, gcs_path):
    client = storage.Client()
    bucket_name = gcs_path.split("/")[2]
    blob_path = "/".join(gcs_path.split("/")[3:])

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    blob.upload_from_filename(local_path)
```

Then call:  
```ruby
</> python

upload_to_gcs(MODEL_PATH, MODEL_GCS_PATH)
```




