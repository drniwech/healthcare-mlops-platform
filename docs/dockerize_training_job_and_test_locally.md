## Dockerize training job and test locally  

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
pandas
scikit-learn
xgboost
google-cloud-bigquery
mlflow
matplotlib
seaborn
joblib
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
