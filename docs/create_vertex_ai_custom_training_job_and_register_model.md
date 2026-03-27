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



