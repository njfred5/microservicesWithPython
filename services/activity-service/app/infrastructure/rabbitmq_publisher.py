import json
import pika
RABBITMQ_URL = "amqp://guest:guest@localhost:5672"
QUEUE = "gamehub.notifications"
def publish_notification(user_id: str, message: str) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body=json.dumps({"user_id": user_id, "message": message}),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()