from kfp.v2 import dsl, compiler
from google.cloud import aiplatform

from components.ingest_component import ingest_op
from components.train_component import train_op
from components.evaluate_component import evaluate_op
from components.register_component import register_model_op

PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"
PIPELINE_ROOT = "gs://healthcare-mlops-data/pipeline-root"


@dsl.pipeline(
    name="healthcare-full-mlops-pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def ml_pipeline():

    ingest_task = ingest_op()

    train_task = train_op(
        input_data=ingest_task.outputs["output_data"]
    )

    eval_task = evaluate_op(
        model=train_task.outputs["model_output"],
        input_data=ingest_task.outputs["output_data"]
    )

    register_task = register_model_op(
        model=train_task.outputs["model_output"]
    )


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="pipeline.json"
    )

    aiplatform.init(project=PROJECT_ID, location=REGION)

    job = aiplatform.PipelineJob(
        display_name="healthcare-full-pipeline-run",
        template_path="pipeline.json",
        pipeline_root=PIPELINE_ROOT,
    )

    job.run()
