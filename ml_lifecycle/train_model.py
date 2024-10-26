import pandas as pd
import pickle
import dvc.api
import os
from src.models.classifier import Classifier

def load_processed_data():
    # Load processed data from DVC
    processed_data_path = dvc.api.get_url('processed_data/processed_data.csv', repo='your_repo_url')
    return pd.read_csv(processed_data_path)

def train_model(data):
    classifier = Classifier(model_path='path/to/your/model.pth')
    classifier.train(data)  # Assume there is a train method
    return classifier

def save_model(model):
    model_path = 'model/model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    # Add model to DVC tracking
    os.system(f"dvc add {model_path}")

if __name__ == "__main__":
    data = load_processed_data()
    model = train_model(data)
    save_model(model)
