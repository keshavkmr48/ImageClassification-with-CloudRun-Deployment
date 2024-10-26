import kfp
from kfp import dsl

def data_preprocessing_op():
    """Pipeline step to preprocess data."""
    return dsl.ContainerOp(
        name="Data Preprocessing",
        image="your_preprocessing_docker_image",
        command=["python", "-m", "ml_lifecycle.data_pipeline"],
        arguments=["--input-data", "/data/input.csv", "--output-data", "/data/preprocessed.csv"],
        file_outputs={"output": "/data/preprocessed.csv"}
    )

def train_model_op(preprocessed_data: str):
    """Pipeline step to train the model."""
    return dsl.ContainerOp(
        name="Train Model",
        image="your_training_docker_image",
        command=["python", "-m", "ml_lifecycle.train_model"],
        arguments=["--train-data", preprocessed_data, "--model-output", "/model/model.pth"],
        file_outputs={"model_output": "/model/model.pth"}
    )

def evaluate_model_op(model_path: str, test_data: str):
    """Pipeline step to evaluate the model."""
    return dsl.ContainerOp(
        name="Evaluate Model",
        image="your_evaluation_docker_image",
        command=["python", "-m", "ml_lifecycle.evaluate_model"],
        arguments=["--model-path", model_path, "--test-data", test_data]
    )

def deploy_model_op(model_path: str):
    """Pipeline step to deploy the model."""
    return dsl.ContainerOp(
        name="Deploy Model",
        image="your_deployment_docker_image",
        command=["python", "-m", "ml_lifecycle.deploy_model"],
        arguments=["--model-path", model_path]
    )

@dsl.pipeline(
    name="ML Lifecycle Pipeline",
    description="Pipeline for end-to-end ML lifecycle: data processing, training, evaluation, and deployment."
)
def ml_pipeline():
    # Data preprocessing step
    preprocess = data_preprocessing_op()
    
    # Train the model step, which depends on the preprocessing step
    train = train_model_op(preprocessed_data=preprocess.output)

    # Evaluate the model step, which depends on the training step
    evaluate = evaluate_model_op(model_path=train.output, test_data="/data/test.csv")
    
    # Deploy the model step, which depends on evaluation
    deploy = deploy_model_op(model_path=train.output)

    # Ensure proper sequence
    evaluate.after(train)
    deploy.after(evaluate)

# Compile the pipeline if running outside of the script context
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(ml_pipeline, 'ml_lifecycle_pipeline.yaml')
