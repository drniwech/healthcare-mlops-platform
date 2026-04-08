## 5. Dockerize training job and test locally  

🎯 Objective
- Package training code into Docker image
- Run locally (same as cloud)
- Prepare for upload to Artifact Registry

🧱 Final Project Structure
```
project-root/
│
├── training/
│   ├── train.py
│   ├── config.py
│   ├── utils.py
│   └── model/
│
├── Dockerfile
├── requirements.txt
└── .dockerignore
```

⚙️ Step 1 — Create requirements.txt
```
# training + pipeline
pandas
numpy
scikit-learn
xgboost
joblib
mlflow
google-cloud-aiplatform
google-cloud-storage
google-cloud-bigquery
shap
```

🧾 Step 2 — Create .dockerignore
```ruby
</> bash
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.git
training/model/
```
🐳 Step 3 — Create Dockerfile
Dockerfile  
```ruby
</>dockerfile
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY training/ ./training/

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run training script
CMD ["python", "training/train.py"]
```

🔐 Step 4 — Handle GCP Credentials (IMPORTANT)

We must pass credentials into the container.

**Option A (recommended for now)**  
```ruby
</> bash

export GOOGLE_APPLICATION_CREDENTIALS="/path/to/mlops-key.json"
```
Then mount into the container:  
```ruby
</>bash

docker run \
-v $GOOGLE_APPLICATION_CREDENTIALS:/app/key.json \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
healthcare-mlops:latest
```

🏗 Step 5 — Build Docker Image
```ruby
</>bash

docker build -t healthcare-mlops:latest .
```

▶️ Step 6 — Run Container Locally
```ruby
</>bash

docker run \
-v $GOOGLE_APPLICATION_CREDENTIALS:/app/key.json \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
healthcare-mlops:latest
```

🔍 Expected Output

Inside logs:
```ruby
Loading feature data from BigQuery...
Training XGBoost model...
Accuracy: 0.78
AUC: 0.84
Training complete with MLflow tracking
```

📁 Check Outputs

After run:
```ruby
</>bash

training/model/
```

We should see:

- model.joblib
- metrics.json
- confusion_matrix.png

🧠 What We Just Achieved

Before:
```
Local Python script
```  
Now:
```
Containerized ML Training Job
``` 
This is EXACTLY what runs in:

- Google Vertex AI Custom Jobs
- Kubernetes
- CI/CD pipelines

⚠️ Common Issues (Fix Fast)  
❌ Authentication error
```
👉 Fix: mount JSON key correctly   
```

❌ BigQuery permission denied

👉 Fix: ensure service account has:
```
- BigQuery Admin
- Storage Admin    
```

❌ Module not found

👉 Fix: rebuild image  
```ruby
</>bash

docker build --no-cache -t healthcare-mlops:latest .
```


