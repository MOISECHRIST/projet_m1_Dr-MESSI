import sys
from django.shortcuts import get_object_or_404
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .RabbitMQ import RabbitMQ_User_Producer
from django.contrib.auth.models import User
from  loguru import logger
from .serializers import PersonSerializer
from rest_framework.response import Response
from .models import Person, Worker, Customer

logger.remove()
logger.add(f"logs_warning.log",
           level="WARNING",
           rotation="500mb")

logger.add(sys.stderr, level="SUCCESS")
logger.add(sys.stderr, level="WARNING")

routing_key = "user."


@receiver(user_logged_in)
def handle_user_logged_in(sender, request, **kwargs):
    action = f"user{request.user.pk}.login"
    producer = RabbitMQ_User_Producer()

    if not request.user.is_authenticated:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

    try:
        user = get_object_or_404(User, id=request.user.pk)
        serializer = PersonSerializer(get_object_or_404(Person, user = user))
        data = serializer.data
        data = {'id_person':data['id'],
                'id_user':data['user'],
                'login_status':"Login"}
        if len(Customer.objects.filter(pk=data['id_person']))==1:
             data['user_type']='Customer'
        else :
             data['user_type']='Worker'
        producer.publish(message=data, routing_key=routing_key + action)
        logger.success(f"Success publishing in {routing_key + action}")
        
    except Exception as e:
        logger.error(f"Error publishing in {routing_key + action} : {e}")
    
    producer.close()

@receiver(user_logged_out)
def handle_user_logged_out(sender, request, **kwargs):
    action = f"user{request.user.pk}.logout"
    producer = RabbitMQ_User_Producer()

    if not request.user.is_authenticated:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

    try:
        user = get_object_or_404(User, id=request.user.pk)
        serializer = PersonSerializer(get_object_or_404(Person, user = user))
        data = serializer.data
        data = {'id_person':data['id'],
                'id_user':data['user'],
                'login_status':"Logout"}
        if len(Customer.objects.filter(pk=data['id_person']))==1:
             data['user_type']='Customer'
        else :
             data['user_type']='Worker'
        producer.publish(message=data, routing_key=routing_key + action)
        logger.success(f"Success publishing in {routing_key + action}")
        
    except Exception as e:
        logger.error(f"Error publishing in {routing_key + action} : {e}")
    
    producer.close()
      