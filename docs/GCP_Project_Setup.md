# Set up GCP project, enable Vertex AI & BigQuery, configure IAM  

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
