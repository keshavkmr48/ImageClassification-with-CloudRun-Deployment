import os
from pathlib import Path

app = "app"
services = "services"
ml_lifecycle = "ml_lifecycle"

list_of_files = [
   # GitHub Actions Workflow
   ".github/workflows/service_management_ci.yaml",  # CI/CD for service management
   ".github/workflows/ml_lifecycle_management_ci.yaml",  # CI/CD for ML lifecycle management

   # Source code structure for services (API and microservices)
   "src/__init__.py",
   "src/data/__init__.py",
   "src/data/gcp_utils.py",
   "src/models/__init__.py", 
   "src/models/classifier.py",
   "src/models/prediction_result.py",

   # FastAPI app files
   f"{app}/__init__.py", 
   f"{app}/config.py", 
   f"{app}/db.py", 
   f"{app}/main.py", 
   f"{app}/entrypoint.sh", 
   f"{app}/migrations/loggers_table.py", 
   f"{app}/migrations/__init__.py", 
   f"{app}/routes/__init__.py", 
   f"{app}/routes/files.py", 




   # Scripts for CloudRun and Docker
   "crun_deploy.sh",
   "Dockerfile",
   "Readme.md",

   # Tests for service management
   "tests/__init__.py",
   "tests/unit/__init__.py",
   "tests/unit/test_unit.py",
   "tests/integration/__init__.py",
   "tests/integration/test_int.py",

   # Requirements for inference services and CI/CD
   "requirements.txt", 
   "requirements_dev.txt",
   "setup.py",
   "setup.cfg",
   "pyproject.toml",
   "tox.ini",

   # ML lifecycle management directories (Airflow/Kubeflow integration)
   f"{ml_lifecycle}/__init__.py",
   f"{ml_lifecycle}/data_pipeline.py",  # Data processing pipeline
   f"{ml_lifecycle}/train_model.py",  # Model training script
   f"{ml_lifecycle}/evaluate_model.py",  # Model evaluation script
   f"{ml_lifecycle}/retrain_model.py",  # Model retraining script
   f"{ml_lifecycle}/model_registry.py",  # Handles model versioning and registry

   # Kubeflow pipelines and Airflow DAGs
   f"{ml_lifecycle}/kubeflow_pipeline.py",
   f"{ml_lifecycle}/airflow_dag.py",

   # Scripts for Kubernetes (if used for model training)
   "k8s/deploy_model_training.yaml",
   "k8s/deploy_inference.yaml",

   # Scripts for ELK stack setup
   "elk_stack/setup_elasticsearch.sh",
   "elk_stack/setup_logstash.sh",
   "elk_stack/setup_kibana.sh",

   # Experiments and notebooks for model development
   "experiments/experiments.ipynb",

   # Separate Dockerfile and requirements for ML lifecycle
   f"{ml_lifecycle}/Dockerfile",
   f"{ml_lifecycle}/requirements_ml.txt",

   # CI/CD for ML lifecycle
   "kubeflow_deploy.sh",  # Script to trigger Kubeflow pipeline
   "airflow_deploy.sh",  # Script to trigger Airflow DAGs
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # create an empty file
