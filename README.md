# healthcare-mlops-platform
Trust-Aware Healthcare Readmission Prediction Platform

## Problem Statement
Predict 30-day hospital readmission risk and monitor model trust, drift, and reliability in production.  

## MLOps Architecture Diagram  

![MLOps Architecture Diagram](https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/Healthcare_MLOps.drawio.png)  

## Project Structure
```
---data_pipeline/
---training/
---pipeline/
---deployment/
---monitoring/
---ci_cd/
---docs/
---README.md
```

	•	Problem
	•	Architecture
	•	Tech Stack
	•	How to Run
	•	Monitoring Strategy
	•	Future Improvements

----------------------------------------------------------------------------------------------

## Implementation Steps  
1. Set up GCP project, enable Vertex AI & BigQuery, configure IAM [(https://github.com/drniwech/healthcare-mlops-platform/blob/index/docs/gcp_project_setup.md)](https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/gcp_project_setup.md).
2. Load synthetic healthcare dataset into BigQuery ([docs/load_a_synthetic_healthcare_dataset.md](https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/load_a_synthetic_healthcare_dataset.md)).
3. Write feature engineering script (https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/feature_engineering_script.md)
4. Build local training script (XGBoost) (https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/build_local_training_script.md)
5. 
