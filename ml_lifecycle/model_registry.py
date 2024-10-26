import os
import dvc.api

def register_model(model_path):
    # Register model with DVC
    os.system(f"dvc add {model_path}")
    os.system("dvc push")  # Push to DVC remote

if __name__ == "__main__":
    register_model('model/model.pkl')
