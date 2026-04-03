# 1. Set up GCP project, enable Vertex AI & BigQuery, configure IAM  

1️⃣ Create a GCP Project

Go to
https://console.cloud.google.com

1. Click **Project Selector**
2. Click **New Project**
3. Enter  
Project name:
**healthcare-mlops-platform**

Leave organization empty if personal.

Click **Create**  

2️⃣ Enable Required Services

Open APIs & Services → Library

Enable these services:

**Service >> Purpose**  
1. Vertex AI   >> ML training + deployment  
2. BigQuery >> Data warehouse  
3. Cloud Storage	>> Data lake  
4. Artifact Registry	>> Docker images  
5. Cloud Build	>> CI/CD  
6. Cloud Logging	>> Monitoring  

Quick way:  

Search each service → **Enable**  

3️⃣ Install CLI (if not installed)

Install
Google Cloud CLI

Mac:
```ruby
</> bash
brew install --cask google-cloud-sdk
```
Then login:
```ruby
</> bash
gcloud auth login
```
Set project
```ruby
</> bash
gcloud config set project healthcare-mlops-platform
```
Verify:
```ruby
</> bash
gcloud config list
```
4️⃣ Create Data Lake Bucket
```ruby
</> bash
gsutil mb -l us-central1 gs://healthcare-mlops-data
```
Verify
```ruby
</> bash
gsutil ls
```
You now have a data lake for training data.  

5️⃣ Create BigQuery Dataset

Open
BigQuery → Create Dataset

Name:
```
healthcare_ml
```
Location
```
US
```
6️⃣ Create Service Account (MLOps pipeline)

Go to

IAM & Admin → Service Accounts

Create:
```
mlops-pipeline-sa
```
Description:
```
MLOps pipeline automation
```
7️⃣ Assign Roles

Add roles:

**Role	>> Reason**
Vertex AI Admin	>> ML training
BigQuery Admin	>> Data access
Storage Admin	>> Data lake
Artifact Registry Admin	>> container images  

8️⃣ Create Key for Local Development

Inside service account

Create key → JSON

Download
```ruby
mlops-key.json
```
Set environment variable:

Mac/Linux
```ruby
export GOOGLE_APPLICATION_CREDENTIALS="mlops-key.json"
```

9️⃣ Test Vertex AI Access

Run:
```ruby
</> bash
gcloud ai models list
```
If it works → setup is correct.  

### Architecture Now Matches the Diagram

We just implemented the first part of the architecture:
```
Data Lake → GCS
Warehouse → BigQuery
ML Platform → Vertex AI
Compute → GKE (later)
```

### Deliverable

We should now have:
```
✔ GCP project
✔ Vertex AI enabled
✔ BigQuery dataset
✔ Cloud Storage data lake
✔ IAM service account
✔ CLI configured
```
