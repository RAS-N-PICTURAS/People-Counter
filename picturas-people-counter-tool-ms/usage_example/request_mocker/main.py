import json
import logging
import os
import random
import time
import uuid
from datetime import datetime

import pika
from pika.exchange_type import ExchangeType

# Configurações
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
PICTURAS_SRC_FOLDER = os.getenv("PICTURAS_SRC_FOLDER", "./usage_example/images/src/")
PICTURAS_OUT_FOLDER = os.getenv("PICTURAS_OUT_FOLDER", "./usage_example/images/out/")

# Configuração de Logs
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)


def message_queue_connect():
    """
    Estabelece conexão com o RabbitMQ.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    return connection, channel


def message_queue_setup(channel):
    """
    Configura o exchange e as filas no RabbitMQ.
    """
    channel.exchange_declare(
        exchange="picturas.tools",
        exchange_type=ExchangeType.direct,
        durable=True,
    )
    channel.queue_declare(queue="results")
    channel.queue_bind(
        queue="results",
        exchange="picturas.tools",
        routing_key="results",
    )

    channel.queue_declare(queue="people-counter-requests")
    channel.queue_bind(
        queue="people-counter-requests",
        exchange="picturas.tools",
        routing_key="requests.people_counter",
    )


def publish_request_message(channel, routing_key, request_id, procedure, parameters):
    """
    Publica uma mensagem de solicitação no RabbitMQ.
    """
    message = {
        "messageId": request_id,
        "timestamp": datetime.now().isoformat(),
        "procedure": procedure,
        "parameters": parameters,
    }

    channel.basic_publish(
        exchange="picturas.tools",
        routing_key=routing_key,
        body=json.dumps(message),
    )

    logging.info("Published request '%s' to '%s'", request_id, routing_key)


def publish_mock_requests_forever():
    """
    Envia solicitações contínuas com base nas imagens da pasta `src`.
    """
    try:
        while True:
            for file_name in os.listdir(PICTURAS_SRC_FOLDER):
                request_id = str(uuid.uuid4())

                people_counter_parameters = {
                    "inputImageURI": os.path.join(PICTURAS_SRC_FOLDER, file_name),
                    "outputImageURI": os.path.join(PICTURAS_OUT_FOLDER, f"processed_{file_name}")
                }

                publish_request_message(channel, "requests.people_counter", request_id, "people_counter", people_counter_parameters)
                time.sleep(random.uniform(2, 5))
    finally:
        connection.close()


if __name__ == "__main__":
    # Conectar ao RabbitMQ
    connection, channel = message_queue_connect()
    # Configurar o exchange e as filas
    message_queue_setup(channel)
    # Publicar solicitações de teste
    publish_mock_requests_forever()
