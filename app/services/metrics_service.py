from prometheus_client import Summary, Counter, start_http_server

# Initialize Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
PREDICTION_COUNTER = Counter('predictions_total', 'Total number of predictions')

class MetricsService:
    def __init__(self):
        # Start Prometheus server on a separate port
        start_http_server(8001)
    
    @REQUEST_TIME.time()
    def track_prediction_time(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    def increment_prediction_count(self):
        PREDICTION_COUNTER.inc()

metrics_service = MetricsService()
