import pika
import json

# RabbitMQ connection URL (matching the Docker Compose configuration)
RABBITMQ_URL = 'amqp://user:password@localhost:5672/'

# Message processing function
def process_message(ch, method, properties, body):
    message = json.loads(body)
    action = message.get('action')

    if action == 'update-data':
        print("Received update-data action")
        print(message)
        # Make a request to the NextJS API to get updated data
        # response = requests.get('https://your-nextjs-api-url/api/data')
        # if response.status_code == 200:
        #     data = response.json()
        #     print(f"Updated data: {data}")
        #     # Handle the data
        # else:
        #     print(f"Failed to fetch data: {response.status_code}")

    elif action == 'update-app':
        print("Received update-app action")
        # Simulate updating the app
        app_version = message['payload'].get('version')
        print(f"Updating app to version {app_version}")
        # Trigger app update logic here

    elif action == 'restart':
        print("Received restart action")
        # Simulate restarting the Raspberry Pi
        print("Restarting Raspberry Pi...")
        # Uncomment the following line if you actually want to reboot the system:
        # os.system("sudo reboot")

    else:
        print(f"Unknown action: {action}")

# Start listening to the RabbitMQ queue
def start_listening(device_id):
    # Use the connection URL for RabbitMQ
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    # Define queue name
    queue_name = f'raspberry-pi-{device_id}'
    channel.queue_declare(queue=queue_name, durable=True)

    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=process_message, auto_ack=True)

    print(f"Raspberry Pi {device_id} is waiting for messages...")
    channel.start_consuming()

# Start listening with the device ID of the Raspberry Pi
start_listening('pi-01')
