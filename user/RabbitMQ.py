import pika
from decouple import config
import json

RABBITMQ_HOST = config("RABBITMQ_HOST")
RABBITMQ_PORT = config("RABBITMQ_PORT")
RABBITMQ_USER = config("RABBITMQ_USER")
RABBITMQ_PASSWORD = config("RABBITMQ_PASSWORD")

class RabbitMQ_User_Producer:
    def __init__(self):
        #parametre de connexion
        self.host = RABBITMQ_HOST
        self.port = RABBITMQ_PORT
        self.user = RABBITMQ_USER
        self.password = RABBITMQ_PASSWORD

        #Connexion au serveur RabbitMQ
        self.credentials = pika.PlainCredentials(self.user, self.password)
        self.connexion = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
               credentials=self.credentials
            )
        )

        #Creation d'un channel
        self.channel = self.connexion.channel()

        #Creation d'un exchange
        self.channel.exchange_declare(
            exchange="user_events",
            exchange_type="topic",
            durable=True
        )

        self.channel.queue_declare(queue="user_queue", durable=True)
        self.channel.queue_bind(exchange="user_events", queue="user_queue", routing_key="user.#")


    def publish(self, message, routing_key):
        #print(f"routing key : {routing_key}")
        #print(f"RabbiMQ data received : \n{message}")
        self.channel.basic_publish(
            exchange="user_events",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

    def close(self):
        self.connexion.close()

if __name__ =="__main__":
    test = RabbitMQ_User_Producer()
    test.publish(message="Creation d'un compte WORKER", routing_key="user.worker.created")
    test.close()