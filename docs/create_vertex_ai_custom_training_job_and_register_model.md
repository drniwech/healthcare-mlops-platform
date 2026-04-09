## 6. Create Vertex AI custom training job and register model  

🎯 Objective
- Push Docker image → Artifact Registry
- Run Vertex AI Custom Training Job
- Register trained model in Model Registry

🧠 Architecture We’re Implementing
```
GCP → Docker → Artifact Registry → Vertex AI Training → Model Registry
```  
This is exactly what companies do.  

⚙️ Step 0 — Create a custom service account  
```bash
gcloud iam service-accounts create vertex-training-sa
```

Grant Roles  
```bash
gcloud projects add-iam-policy-binding healthcare-mlops-platform \
  --member="serviceAccount:vertex-training-sa@healthcare-mlops-platform.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding healthcare-mlops-platform \
  --member="serviceAccount:vertex-training-sa@healthcare-mlops-platform.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

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

🏗 Step 3 — Tag & Build Image in GCP (correct CPU)
```ruby
</> bash

gcloud builds submit --tag \
us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest
```
It automatically:
```
- Builds image in GCP (correct CPU) ✅
- Tags it correctly ✅
- Pushes to Artifact Registry ✅
```

🧪 Step 4 — Run Vertex AI Custom Training Job
```ruby
</> bash

gcloud ai custom-jobs create \
--region=us-central1 \
--display-name=healthcare-training-job \
--worker-pool-spec=machine-type=e2-standard-4,replica-count=1,container-image-uri=us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest  \
--service-account=vertex-training-sa@healthcare-mlops-platform.iam.gserviceaccount.com
```

🔍 What Happens Now

Vertex AI will:

- Build Docker image in GCP.
   - You built your image on a Mac (likely Apple Silicon or different arch), so:
    -  Local build = linux/arm64 ❌
    -  Vertex AI requires = linux/amd64 ✅
    -  👉 Result: Vertex cannot pull/run your image
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

🏷 Step 6 — Register Model in Vertex AI

After training completes:
```ruby
</> bash

gcloud ai models upload \
--region=us-central1 \
--display-name=healthcare-readmission-model \
--artifact-uri=gs://healthcare-mlops-data/models/ \
--container-image-uri=us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-5:latest
```

🧠 What We Just Built
```
Training Job → GCS → Vertex Model Registry
```
This is the production ML lifecycle.  

✅ End of Day Deliverable

We now have:

- ✔ Docker image in Artifact Registry
- ✔ Training job running on Vertex AI
- ✔ Model saved in GCS
- ✔ Model registered in Vertex AI


