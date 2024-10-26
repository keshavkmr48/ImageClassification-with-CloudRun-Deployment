from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ml_lifecycle.data_pipeline import run_data_pipeline
from ml_lifecycle.train_model import train_model
from ml_lifecycle.evaluate_model import evaluate_model
from ml_lifecycle.deploy_model import deploy_model

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False
}

def data_preprocessing_task():
    X_train, X_test, y_train, y_test = run_data_pipeline("path/to/input.csv", "target_column")
    return X_train, X_test, y_train, y_test

def train_model_task(**kwargs):
    X_train, X_test, y_train, y_test = kwargs['task_instance'].xcom_pull(task_ids='data_preprocessing')
    train_model(X_train, y_train, "path/to/model.pth")

def evaluate_model_task(**kwargs):
    X_train, X_test, y_train, y_test = kwargs['task_instance'].xcom_pull(task_ids='data_preprocessing')
    evaluate_model("path/to/model.pth", X_test, y_test)

def deploy_model_task():
    deploy_model("path/to/model.pth")

with DAG('ml_lifecycle_dag', default_args=default_args, schedule_interval='@daily') as dag:

    # Task 1: Data preprocessing
    data_preprocessing = PythonOperator(
        task_id='data_preprocessing',
        python_callable=data_preprocessing_task,
    )

    # Task 2: Train model (depends on preprocessing)
    train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_model_task,
        provide_context=True,
    )

    # Task 3: Evaluate model (depends on training)
    evaluate_model = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model_task,
        provide_context=True,
    )

    # Task 4: Deploy model (depends on evaluation)
    deploy_model = PythonOperator(
        task_id='deploy_model',
        python_callable=deploy_model_task,
    )

    # Setting the task dependencies
    data_preprocessing >> train_model >> evaluate_model >> deploy_model
