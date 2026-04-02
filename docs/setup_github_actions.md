## Set up GitHub Actions (lint, Docker build, pipeline trigger)

🎯 Objective  

Set up CI/CD to:  

- Lint Python code
- Build Docker image
- Push to Google Artifact Registry
- Trigger Google Vertex AI Pipeline

🧱 Step 1 — Repo Structure  

```ruby
</> bash

.github/
└── workflows/
    └── mlops-ci.yml
```

🔐 Step 2 — Add GitHub Secrets  

Go to:  
```
GitHub → Settings → Secrets → Actions
```
Add:  
```
Secret Name      | Value                                
---------------- | -------------------------  
GCP_PROJECT_ID   | healthcare-mlops-platform 
GCP_REGION       | us-central1               
GCP_SA_KEY       | (paste our JSON key)     
```

👉 Use our service account JSON  

🧾 Step 3 — Create Workflow File  
.github/workflows/mlops-ci.yml  
```ruby
</> YAML

name: MLOps CI/CD Pipeline

on:
  push:
    branches: [ "main" ]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  REGION: ${{ secrets.GCP_REGION }}
  REPO: mlops-repo
  IMAGE: healthcare-mlops

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    # ✅ Setup Python
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    # ✅ Install dependencies
    - name: Install dependencies
      run: |
        pip install flake8

    # ✅ Lint code
    - name: Lint with flake8
      run: |
        flake8 . --max-line-length=120

    # 🔐 Authenticate to GCP
    - name: Authenticate to GCP
      uses: google-github-actions/auth@v1
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}

    # ☁️ Setup gcloud
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v1

    # 🐳 Configure Docker
    - name: Configure Docker
      run: |
        gcloud auth configure-docker $REGION-docker.pkg.dev

    # 🏗 Build Docker image
    - name: Build Docker image
      run: |
        docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest .

    # 🚀 Push Docker image
    - name: Push Docker image
      run: |
        docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest

    # 🔁 Trigger Vertex AI Pipeline
    - name: Trigger Vertex AI Pipeline
      run: |
        python pipeline/pipeline.py
```

🧠 What This Does  

Every time we push to main: 
```
1. Lint code
2. Build Docker image
3. Push to Artifact Registry
4. Run pipeline
```
👉 Fully automated ML workflow.  

⚠️ Important Fix (VERY IMPORTANT)  

Our pipeline.py must NOT auto-run locally like:  
```ruby
</> python

job.run()
```
👉 Modify it to accept execution only when called explicitly  

Better approach:  
```ruby
</> python

if __name__ == "__main__":
    import sys

    if "run" in sys.argv:
        job.run()
```

Then in GitHub Actions:  
```ruby
</> YAML

python pipeline/pipeline.py run
```

🧠 Real-World Insight  

This setup mimics:  
```
Company System    |    Our Setup
----------------  | -------------------------
CI/CD pipeline    |    GitHub Actions
Container registry    |    Artifact Registry
ML pipeline    |    Vertex AI
Deployment trigger    |    Git push
```
👉 This is enterprise MLOps  

💰 Cost Awareness  

This step may:  
```
Trigger pipeline runs
Use compute resources
```
👉 Add branch filter later (e.g., only on release)  

🚀 What We Just Built  
```
Code → CI/CD → Docker → Cloud → ML Pipeline
```
👉 This is end-to-end automated MLOps.  

🎯 Final Status  

We now have:
```
✔ Data pipeline
✔ Feature engineering
✔ Training
✔ MLflow tracking
✔ Docker
✔ Vertex AI pipeline
✔ Endpoint deployment
✔ Prediction client
✔ CI/CD automation
```
👉 This is top-tier portfolio level.  

