# 15. Vertex AI Model Monitoring

## 🎯 Objective

Enable **Vertex AI Model Monitoring** to:  
- Detect **data drift**
- Monitor **feature distribution changes**
- Establish a foundation for **production ML observability**

------------------------------------------------------------------------

## 🧱 Architecture Context

Current system:  
- Vertex AI Endpoint (deployed model) 
- FastAPI inference layer 
- Logging (prediction + confidence) 
- SHAP explainability

👉 Today: Add **native monitoring layer (Vertex AI)**

------------------------------------------------------------------------

🧱 Clean Project Structure 
```
project-root/
│
├── api/
│   └── app.py                  ✅ FastAPI (no change)
│
├── prediction/
│   └── predict.py              ✅ Vertex call (no change)
│
├── monitoring/
│   └── setup_monitoring.py     🆕 NEW (Day 17)
│
├── common/
├── config.py
```
------------------------------------------------------------------------

## 🧠 Why Vertex Model Monitoring?

-   Fully managed by GCP
-   No additional infrastructure
-   Integrated with deployed endpoints
-   Supports:
    -   Feature drift detection
    -   Training-serving skew detection

------------------------------------------------------------------------

## 🔄 Step 1: Prepare Baseline Dataset

Vertex requires a **baseline dataset** (training data). This file will be used in Step 3.  

### Example (GCS path)

``` bash
gs://your-bucket/data/training_data.csv
```

Requirements: - Same schema as prediction input - Clean, representative
data

------------------------------------------------------------------------

## 🔄 Step 2: Enable Model Monitoring

### Python Setup  

New File: `/monitoring/setup_monitoring.py`  

``` python
from google.cloud import aiplatform

aiplatform.init(project=PROJECT_ID, location=REGION)
```

------------------------------------------------------------------------

### Create Monitoring Job

``` python
job = aiplatform.ModelDeploymentMonitoringJob.create(
    display_name="model-monitoring-job",
    endpoint=ENDPOINT_ID,
    logging_sampling_strategy={
        "random_sample_config": {"sample_rate": 0.8}
    },
    schedule_config={
        "monitor_interval": 3600
    },
    alert_config={
        "email_alert_config": {
            "user_emails": ["your_email@example.com"]
        }
    }
)
```

------------------------------------------------------------------------

## 🔄 Step 3: Configure Drift Detection

``` python
drift_config = {
    "numerical_threshold_config": {"value": 0.05},
    "categorical_threshold_config": {"value": 0.1}
}
```

------------------------------------------------------------------------

### Attach to Monitoring Job

``` python
job = aiplatform.ModelDeploymentMonitoringJob.create(
    display_name="model-monitoring-job",
    endpoint=ENDPOINT_ID,
    objective_configs=[
        {
            "training_dataset": {
                "gcs_source": {"uris": ["gs://your-bucket/data/training_data.csv"]},
                "data_format": "csv"
            },
            "drift_detection_config": drift_config
        }
    ]
)
```

------------------------------------------------------------------------

## 🔄 Step 4: Deploy with Logging Enabled

``` python
endpoint.deploy(
    model=model,
    deployed_model_display_name="model-v1",
    traffic_percentage=100,
    enable_access_logging=True
)
```

------------------------------------------------------------------------

## 📊 Step 5: View Monitoring Results

Vertex AI → Endpoints → Monitoring

------------------------------------------------------------------------

## 🧪 Step 6: Simulate Drift (Preview)

``` json
{
  "age": 90,
  "num_procedures": 10,
  "num_medications": 50,
  "days_in_hospital": 30
}
```

------------------------------------------------------------------------

## 📧 Alerts

Configured via email in alert_config (Step 2)  

------------------------------------------------------------------------

## 🧠 Key Design Decisions

-   Managed monitoring (Vertex AI)
-   Hourly checks balance cost/performance
-   Conservative thresholds reduce noise


------------------------------------------------------------------------

## ✅ Deliverables

-   Monitoring job created
-   Drift detection enabled
-   Alerts configured
-   Logging verified


