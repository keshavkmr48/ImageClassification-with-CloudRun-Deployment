import os
from pydantic import BaseSettings

class Settings(BaseSettings):


    # GCP Configurations
    GCP_BUCKET_NAME: str = os.getenv("GCP_BUCKET_NAME", "your-gcp-bucket-name")
    GCP_PROJECT_ID:str = os.getenv('GCP_PROJECT_ID', 'my-gcp-project-id')
    GCP_CREDENTIALS_PATH: str = os.getenv("GCP_CREDENTIALS_PATH", "path-to-gcp-credentials.json")

    # RabbitMQ Configurations
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    RABBITMQ_QUEUE : str = os.getenv('RABBITMQ_QUEUE', 'image_queue')
    # Database Configurations
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/image_classification")

    # Other Configurations
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/image_classifier.pth")
    API_PREFIX: str = "/api"

    class Config:
        env_file = ".env"  # Load environment variables from .env file

# Instantiate settings for use across the app
settings = Settings()
