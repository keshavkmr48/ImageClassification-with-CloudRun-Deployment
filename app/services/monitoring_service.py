import time
from metrics_service import metrics_service
from logging_service import logging_service

class MonitoringService:
    def monitor_request(self, func, *args, **kwargs):
        start_time = time.time()
        result = metrics_service.track_prediction_time(func, *args, **kwargs)
        end_time = time.time()
        latency = end_time - start_time
        logging_service.log_info(f"Request latency: {latency} seconds")
        return result

monitoring_service = MonitoringService()
