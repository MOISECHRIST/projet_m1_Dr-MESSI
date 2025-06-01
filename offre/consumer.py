import pika
import json
import threading
from decouple import config
from .models import Worker, Customer, Person, Service
from loguru import logger
import sys
from django.shortcuts import get_object_or_404

logger.remove()
logger.add(f"logs_warning.log",
           level="WARNING",
           rotation="500mb")

logger.add(sys.stderr, level="SUCCESS")
logger.add(sys.stderr, level="WARNING")

RABBITMQ_HOST = config("RABBITMQ_HOST")
RABBITMQ_PORT = config("RABBITMQ_PORT")
RABBITMQ_USER = config("RABBITMQ_USER")
RABBITMQ_PASSWORD = config("RABBITMQ_PASSWORD")

DESTINATAIRE_SERVICE = "offre"
SENDER = "user_offre"
SENDER_SERVICE = "user"
KEYS = [".worker.create_", ".customer.create_", ".user.login_", ".user.logout_", ".worker.delete_", ".customer.delete_"]
def handle_worker_event(routing_key, data):
    if "create" in routing_key:
        object = Worker.objects.create(id_person=data["id"],
                                       id_user = data["user"],
                                       login_status="Login",
                                       user_type="Worker")
        object.save()
        logger.success(f"Success consuming in {routing_key}")
    elif "delete" in routing_key:
        object=Worker.objects.filter(id=data)
        object.delete()
        logger.success(f"Success consuming in {routing_key}")

def handle_customer_event(routing_key, data):
    print(data)
    if "create" in routing_key:
        object = Customer.objects.create(id_person=data["id"],
                                       id_user=data["user"],
                                       login_status="Login",
                                       user_type="Customer")
        object.save()
        logger.success(f"Success consuming in {routing_key}")
    elif "delete" in routing_key:
        object = get_object_or_404(Person,id_person=data['id'])
        object.delete()
        logger.success(f"Success consuming in {routing_key}")
def handle_person_event(routing_key, data):
    if "login" in routing_key:
        print(data)
        object = get_object_or_404(Person,id_person=data['id_person'])
        object.login_status=data["login_status"]
        object.save()
        logger.success(f"Success consuming in {routing_key}")
    elif "logout" in routing_key:
        print(data)
        object = get_object_or_404(Person,id_person=data['id_person'])
        object.login_status=data["login_status"]
        object.save()
        logger.success(f"Success consuming in {routing_key}")

def handle_service_event(routing_key, data):
    if "create" in routing_key:
        object = Service.objects.create(service_id=data["id"],
                                        service_name = data['service_name'])
        object.save()
        logger.success(f"Success consuming in {routing_key}")
    elif "delete" in routing_key:
        object = get_object_or_404(Person,service_id=data['id'])
        object.delete()
        logger.success(f"Success consuming in {routing_key}")

def start_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=int(RABBITMQ_PORT), credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=SENDER + "_events", exchange_type="topic", durable=True)
    queue_name = SENDER + "_queue"
    channel.queue_declare(queue=queue_name, durable=True)

    # Bind to relevant routing keys
    keys = [SENDER_SERVICE +i+ DESTINATAIRE_SERVICE for i in KEYS]
    for key in keys:
        channel.queue_bind(exchange= SENDER + "_events", queue=queue_name, routing_key=key)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages.")
    channel.start_consuming()

def callback(ch, method, properties, body):
    data = json.loads(body)
    routing_key = method.routing_key

    parts = routing_key.split(".")
    if len(parts) < 3:
        return

    classe = parts[1]
    action_dest = parts[2]

    if "_" not in action_dest:
        return

    action, destinataire = action_dest.split("_")

    # Ne traiter que si le message est destiné à ce microservice
    if destinataire != DESTINATAIRE_SERVICE :
        return

    # Dispatcher selon la classe
    if classe == "worker":
        handle_worker_event(action, data)
    elif classe == "customer":
        handle_customer_event(action, data)
    elif classe == "user":
        handle_person_event(action, data)
    elif classe == "servicesprovided":
        handle_service_event(action, data)