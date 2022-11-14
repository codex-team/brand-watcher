import pika


class Broker:
    """
    The Broker has methods to work with message broker
    :param host - rabbitmq host
    :param port - rabbitmq port
    :param queue_name - queue name for crawler
    """
    def __init__(self, host, port, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue_name)

    def send(self, message: str):
        """
        Send data to queue
        :param message: message to send
        """

        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
