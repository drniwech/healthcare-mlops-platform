from kfp.v2.dsl import component

@component(
    base_image="us-central1-docker.pkg.dev/healthcare-mlops-platform/mlops-repo/healthcare-mlops:latest"
)
def train_model_op():
    import subprocess

    # Run your existing training script inside a container
    subprocess.run(["python", "training/train.py"], check=True)
