from kfp.v2 import dsl
from kfp.v2 import compiler
from google.cloud import aiplatform

from components.train_component import train_model_op


PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"
PIPELINE_ROOT = "gs://healthcare-mlops-data/pipeline-root"


@dsl.pipeline(
    name="healthcare-mlops-pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def ml_pipeline():
    train_task = train_model_op()


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="pipeline.json"
    )

    aiplatform.init(project=PROJECT_ID, location=REGION)

    job = aiplatform.PipelineJob(
        display_name="healthcare-mlops-pipeline-run",
        template_path="pipeline.json",
        pipeline_root=PIPELINE_ROOT,
    )

    job.run()
