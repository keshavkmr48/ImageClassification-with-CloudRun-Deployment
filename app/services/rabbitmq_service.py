import pika
import json

RABBITMQ_URL = "amqp://user:password@rabbitmq_host"  # Replace with your RabbitMQ connection URL

def publish_image_buffer(image_buffer: bytes, file_name: str):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='image_predictions')

    # Create message with image buffer and file name
    message = {
        'file_name': file_name,
        'image_buffer': image_buffer.decode('latin-1')  # Encode the bytes for JSON compatibility
    }

    channel.basic_publish(exchange='', routing_key='image_predictions', body=json.dumps(message))
    connection.close()

def consume_image_buffer():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue='image_predictions')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        # Here, you would call the prediction function using the message data
        # Example: predict(message['file_name'], message['image_buffer'].encode('latin-1'))

    channel.basic_consume(queue='image_predictions', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
