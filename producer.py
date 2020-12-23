import json

import pika

import settings


def set_up_connection():
    params = pika.URLParameters(settings.RABBIT_MQ_URL)

    connection = pika.BlockingConnection(params)

    return connection.channel()


def publish_sale_alert(method: str, message: str):
    channel = set_up_connection()

    properties = pika.BasicProperties(method)

    body = {
        "message": message,
    }

    channel.basic_publish(
        exchange="",
        routing_key="sale_alerts",
        body=json.dumps(body),
        properties=properties,
    )

    channel.close()
