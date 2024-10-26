import json
import pandas as pd
import pickle
import dvc.api
import os
from src.models.classifier import Classifier

def load_model():
    model_path = 'model/model.pkl'
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def load_processed_data():
    processed_data_path = dvc.api.get_url('processed_data/processed_data.csv', repo='your_repo_url')
    return pd.read_csv(processed_data_path)

def evaluate_model(model, data):
    # Implement evaluation logic (e.g., accuracy, precision)
    metrics = {
        'accuracy': 0.95,  # Replace with actual computation
        'precision': 0.93,  # Replace with actual computation
    }
    return metrics

def save_metrics(metrics):
    metrics_path = 'evaluation_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)

    # Add metrics to DVC tracking
    os.system(f"dvc add {metrics_path}")

if __name__ == "__main__":
    model = load_model()
    data = load_processed_data()
    metrics = evaluate_model(model, data)
    save_metrics(metrics)
