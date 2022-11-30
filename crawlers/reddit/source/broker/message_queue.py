import pika
import logging

logging.getLogger('pika').setLevel(logging.WARNING)


class Broker:
    """
    The Broker has methods to work with message broker
    :param rabbitmq_url - connection url for rabbitmq
    :param queue_name - queue name for crawler
    """
    def __init__(self, rabbitmq_url, queue_name):
        self.connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue_name)

    def send(self, message: str):
        """
        Send data to queue
        :param message: message to send
        """

        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)