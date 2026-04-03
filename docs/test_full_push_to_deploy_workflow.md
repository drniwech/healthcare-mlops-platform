## 12. Test full push-to-deploy workflow  

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

🔍 Step 5 — Validate Each Component  

Click pipeline run and check:  
```
Ingest → Train → Evaluate → Register
```
All should be:  
```
✔ Green (success)
```

🔍 Step 6 — Verify Model Registry  

Go to:  

👉 Vertex AI → Models  

Check:  

- New version created
- Model name: healthcare-readmission-model

🧠 What We Just Validated
```
Code Push → CI/CD → Container → Pipeline → Model Registry
```
👉 This is a true production workflow.

-------------------------------------------------------

⚠️ Common Failures (and Fixes)  
❌ Authentication error  
```
Permission denied  
```
👉 Fix:

- Check GCP_SA_KEY
- Check IAM roles

❌ Docker push fails  
```
unauthorized  
```
👉 Fix:
```
</> bash

gcloud auth configure-docker
```

❌ Pipeline fails at ingest  

👉 Likely:  

- BigQuery permission issue  
- Wrong dataset/table name

❌ Module import error (common)  

👉 Fix:  

- Ensure __init__.py exists
- Ensure Docker image includes all code

🔥 Success Criteria (All Must Pass)  

✔ GitHub Actions completes  
✔ Docker image pushed  
✔ Pipeline triggered  
✔ Pipeline succeeds  
✔ Model registered  

🏆 What We Achieved  

We now have:  
```
Fully automated ML system triggered by git push
```
This is what companies call:  

👉 Continuous Training Pipeline (CT)  
👉 CI/CD for ML  


