import logging
from elasticsearch import Elasticsearch

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoggingService:
    def __init__(self):
        # Initialize Elasticsearch client
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def log_info(self, message):
        logging.info(message)
        self._log_to_elasticsearch(message, "info")

    def log_error(self, message):
        logging.error(message)
        self._log_to_elasticsearch(message, "error")

    def _log_to_elasticsearch(self, message, log_level):
        # Insert log into Elasticsearch
        doc = {
            'message': message,
            'log_level': log_level
        }
        self.es.index(index="service-logs", body=doc)

logging_service = LoggingService()
