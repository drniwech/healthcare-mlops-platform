from kfp.v2.dsl import component, Input, Model


@component
def register_model_op(model: Input[Model]):
    from google.cloud import aiplatform

    aiplatform.init(
        project="healthcare-mlops-platform",
        location="us-central1")

    aiplatform.Model.upload(
        display_name="healthcare-readmission-model",
        artifact_uri=model.path,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-5:latest",
    )
