from kfp.v2 import dsl, compiler
from google.cloud import aiplatform

from components.ingest_component import ingest_op
from components.train_component import train_op
from components.evaluate_component import evaluate_op
from components.register_component import register_model_op

# ================================
# Config
# ================================
PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"
PIPELINE_ROOT = "gs://healthcare-mlops-data/pipeline-root"
VERTEX_SERVICE_ACCOUNT = "vertex-training-sa@healthcare-mlops-platform.iam.gserviceaccount.com"

# ================================
# Pipeline Definition
# ================================
@dsl.pipeline(
    name="healthcare-full-mlops-pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def ml_pipeline():
    # Step 1: Ingest
    ingest_task = ingest_op()

    # Step 2: Train
    train_task = train_op(
        input_data=ingest_task.outputs["output_data"]
    )

    # Step 3: Evaluate
    eval_task = evaluate_op(
        model=train_task.outputs["model_output"],
        input_data=ingest_task.outputs["output_data"]
    )

    # Step 4: Register Model
    register_task = register_model_op(
        model=train_task.outputs["model_output"]
    )

    # (Optional future) Add dependency explicitly
    
    # Ensures model is evaluated before registration
    register_task.after(eval_task)


# ================================
# Compile Pipeline
# ================================
def compile_pipeline():
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="pipeline.json"
    )
    print("Pipeline compiled to pipeline.json")


# ================================
# Run Pipeline
# ================================
def run_pipeline():
    aiplatform.init(project=PROJECT_ID, location=REGION)

    job = aiplatform.PipelineJob(
        display_name="healthcare-full-pipeline-run",
        template_path="pipeline.json",
        pipeline_root=PIPELINE_ROOT,
    )

    job.run(service_account=VERTEX_SERVICE_ACCOUNT)
    print("Pipeline submitted to Vertex AI")


# ================================
# Entry Point (SAFE)
# ================================
if __name__ == "__main__":
    import sys

    # Always compile first
    compile_pipeline()

    # Only run when explicitly requested
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_pipeline()
    else:
        print("Pipeline compiled. Use 'python pipeline/pipeline.py run' to execute.")
