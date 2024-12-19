import pika
import json

# RabbitMQ connection URL (same as the one used in Docker Compose)
RABBITMQ_URL = 'amqp://user:password@localhost:5672/'

# Function to send a message to the RabbitMQ queue
def send_message_to_queue(queue_name, message):
    # Connect to RabbitMQ using the URL parameters
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    # Declare the queue (it will only be created if it doesn't already exist)
    channel.queue_declare(queue=queue_name, durable=True)

    # Send the message as a JSON object
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )

    print(f"Sent message to queue {queue_name}: {message}")

    # Close the connection
    connection.close()

# Example usage
if __name__ == '__main__':
    queue_name = 'raspberry-pi-pi-01'  # Name of the queue to send the message to
    message = {
        'action': 'update-data',
        'payload': {
            'data': 'This is the updated data'
        }
    }

    send_message_to_queue(queue_name, message)
