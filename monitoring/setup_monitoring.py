from google.cloud import aiplatform
from config import PROJECT_ID, REGION, ENDPOINT_ID, MODEL_ID

aiplatform.init(project=PROJECT_ID, location=REGION)

# Load endpoint object
endpoint = aiplatform.Endpoint(ENDPOINT_ID)

# Load model object
model = aiplatform.Model(MODEL_ID)

# Create monitoring job
job = aiplatform.ModelDeploymentMonitoringJob.create(
    display_name="model-monitoring-job",
    endpoint=ENDPOINT_ID,
    logging_sampling_strategy={
        "random_sample_config": {"sample_rate": 0.8}
    },
    schedule_config={
        "monitor_interval": {"seconds": 3600}
    },
    alert_config={
        "email_alert_config": {
            "user_emails": ["your_email@example.com"]
        }
    },
    objective_configs=[
        {
            "training_dataset": {
                "gcs_source": {
                    "uris": ["gs://your-bucket/data/training_data.csv"]
                },
                "data_format": "csv"
            },
            "drift_detection_config": {
                "numerical_threshold_config": {"value": 0.05},
                "categorical_threshold_config": {"value": 0.1}
            }
        }
    ]
)

# Deploy model with logging enabled
endpoint.deploy(
    model=model,
    deployed_model_display_name="model-v1",
    traffic_percentage=100,
    enable_access_logging=True
)
