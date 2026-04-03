## 14. Test full push-to-deploy workflow  

🎯 Objective 

Verify end-to-end automation works without manual steps.  

✅ Pre-Flight Checklist (Do This First)  

Before pushing, confirm:  

1️⃣ GitHub Secrets (Repo-level)  
```
- GCP_PROJECT_ID
- GCP_REGION
- GCP_SA_KEY
```

2️⃣ Service Account Permissions  

Our service account must have:  
```
- Vertex AI Admin
- Storage Admin
- Artifact Registry Writer
```
👉 If missing → pipeline will fail  

3️⃣ Required APIs Enabled  

In our GCP project:  
```
- Vertex AI API
- Artifact Registry API
- BigQuery API
```

4️⃣ Dockerfile Exists  

At repo root:
```
</> bash

Dockerfile
```

🚀 Step 1 — Make a Small Change  

Trigger CI/CD with a safe change:  
```ruby
</> bash

git add .
git commit -m "Test CI/CD pipeline trigger"
git push origin main
```

🔍 Step 2 — Watch GitHub Actions  

Go to:  

👉 Repo → Actions tab

We should see:  
```
MLOps CI/CD Pipeline running...
```

🧪 Step 3 — Verify Each Stage  
✅ Stage 1 — Lint  

✔ Should pass quickly  
❌ If fails → fix formatting  

✅ Stage 2 — Docker Build  

Look for:  
```
Successfully built image
```

✅ Stage 3 — Push to Google Artifact Registry  

Look for:  
```
pushed
```

✅ Stage 4 — Pipeline Trigger  

Look for:  
```
Pipeline submitted to Vertex AI
```

🔍 Step 4 — Verify Pipeline in Google Vertex AI  

Go to:  

👉 Vertex AI → Pipelines  

We should see:  

- healthcare-full-pipeline-run
- Status: Running or Completed

