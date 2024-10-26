from google.cloud import storage
from ...app.config import config
import os

class GCPUtils:
    def __init__(self):
        self.client = storage.Client(project=config.GCP_PROJECT_ID)
        self.bucket = self.client.bucket(config.GCP_BUCKET_NAME)
    
    def upload_to_gcp(self, file_name: str, file_data: bytes):
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(file_data)
        print(f"Uploaded {file_name} to GCP bucket {config.GCP_BUCKET_NAME}")

gcp_utils = GCPUtils()
