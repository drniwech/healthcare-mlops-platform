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
1. Set up GCP project, enable Vertex AI & BigQuery, configure IAM [(docs/gcp_project_setup.md)](https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/gcp_project_setup.md).
2. Load synthetic healthcare dataset into BigQuery [(docs/load_a_synthetic_healthcare_dataset.md)](https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/load_a_synthetic_healthcare_dataset.md).
3. Write feature engineering script [(docs/feature_engineering_script.md)](https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/feature_engineering_script.md)
4. Build local training script (XGBoost) ([docs/build_local_training_script.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/build_local_training_script.md)
5. Dockerize training job and test locally ([docs/dockerize_training_job_and_test_locally.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/dockerize_training_job_and_test_locally.md)
6. Create Vertex AI custom training job and register model ([docs/create_vertex_ai_custom_training_job_and_register_model.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/create_vertex_ai_custom_training_job_and_register_model.md)
7. Convert training into pipeline component ([docs/convert_training_into_pipeline_component.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/convert_training_into_pipeline_component.md)
8. Build full pipeline: Ingest → Train → Evaluate → Register ([docs/build_end_to_end_mlops_pipeline.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/build_end_to_end_mlops_pipeline.md)
9. Deploy model to Vertex endpoint ([docs/deploy_model_to_vertex_endpoint.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/deploy_model_to_vertex_endpoint.md)
10. Write prediction script for endpoint testing ([docs/write_prediction_script_for_endpoint_testing.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/write_prediction_script_for_endpoint_testing.md)
11. Set up GitHub Actions (lint, Docker build, pipeline trigger) ([docs/setup_github_actions.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/setup_github_actions.md)
12. Test full push-to-deploy workflow ([docs/test_full_push_to_deploy_workflow.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/test_full_push_to_deploy_workflow.md)
13. Integrate SHAP explainability ([docs/integrate_shap_explainability.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/integrate_shap_explainability.md)
14. Logging Prediction Confidence Scores ([docs/log_prediction_confidence_scores.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/log_prediction_confidence_scores.md)
15. Vertex AI Model Monitoring ([docs/enable_vertex_model_monitoring.md]https://github.com/drniwech/healthcare-mlops-platform/blob/main/docs/enable_vertex_model_monitoring.md)
