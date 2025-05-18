import sys
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from .producer import RabbitMQ_User_Producer
from  loguru import logger
from django.shortcuts import get_object_or_404

logger.remove()
logger.add(f"logs_warning.log",
           level="WARNING",
           rotation="500mb")

logger.add(sys.stderr, level="SUCCESS")
logger.add(sys.stderr, level="WARNING")
routing_key = "user."
list_services = ["publication", "abonnement", "offre", "recommendation", "messagerie"]
list_queue = ["user_publication_queue", "user_abonnement_queue", "user_offre_queue", "user_recommendation_queue", "user_messagerie_queue"]
list_exchange = ["user_publication_events", "user_abonnement_events", "user_offre_events", "user_recommendation_events", "user_messagerie_events"]

class MeViewSet(viewsets.ViewSet):

    def list(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        try:
            user = user = get_object_or_404(User, id=request.user.pk)
            user_data = UserSerializer(user).data
            return Response(user_data)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)

    def retrieve(self, request, pk):
        user = User.objects.get(id=pk)

        if user != request.user:
            return Response({"message": "User not connected"}, status=403)

        data = UserSerializer(user).data
        return Response({"message": "User connected"}, status=200)

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
    def create(self, request):
        password = request.data.get("password")
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")

        user = User.objects.create(username = username, first_name=first_name, last_name=last_name,
                                   email=email)
        user.set_password(password)
        user.save()
        data = {"id":user.pk,
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email": user.email,
                "password":user.password}
        return Response(data)
    
    def update(self, request, pk):
        user = get_object_or_404(User, id=pk)
        password = request.data.get("password")
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")

        user.username = username
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        if user.check_password(password):
            user.set_password(password)
        user.save()
        data = {"id":user.pk,
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email": user.email,
                "password":user.password}
        return Response(data)
    
    def partial_update(self, request, pk):
        user = get_object_or_404(User, id=pk)
        password = request.data.get("password")
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")

        user.username = username
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        if user.check_password(password):
            user.set_password(password)
        
        user.save()
        data = {"id":user.pk,
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email": user.email,
                "password":user.password}
        return Response(data)


    def destroy(self, request, pk):
        object = User.objects.get(id=pk)
        action = "person.delete"
        producer = [RabbitMQ_User_Producer(queue=queue, exchange=exchange) for queue, exchange in zip(list_queue, list_exchange)]

        try:
            person = Person.objects.get(user=object)
            publish = True

        except Exception as e :
            logger.error(f"Error no Person object is related to user {object.pk}")
            publish = False

        if publish:
            try :
                object.delete()
                for i, service in enumerate(list_services):
                    producer[i].publish(message=pk, routing_key=routing_key + action +"_"+ service)
                    logger.success(f"Success publishing in {routing_key + action + '_' + service}")
            except Exception as e:
                logger.error(f"Error publishing in {routing_key + action} : {e}")
            finally:
                for p in producer:
                    p.close()
        else :
            object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []

class ServicesProvidedViewSet(viewsets.ModelViewSet):
    queryset = ServicesProvided.objects.all()
    serializer_class = ServicesProvidedSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ServicesProvidedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "servicesprovided.create_recommendation"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key+action)
            logger.success(f"Success publishing in {routing_key+action }")
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = ServicesProvided.objects.get(id=pk)

        action = "servicesprovided.delete_recommendation"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

class PreferenceAreaViewSet(viewsets.ModelViewSet):
    queryset = PreferenceArea.objects.all()
    serializer_class = PreferenceAreaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = PreferenceAreaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "preferencearea.create_recommendation"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key+action)
            logger.success(f"Success publishing in {routing_key+action}")
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def update(self, request, pk):
        object = PreferenceArea.objects.get(id=pk)
        serializer = PreferenceAreaSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "preferencearea.update_recommendation"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def partial_update(self, request, pk):
        object = PreferenceArea.objects.get(id=pk)
        serializer = PreferenceAreaSerializer(instance=object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        action = "preferencearea.partialupdate_recommendation"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = PreferenceArea.objects.get(id=pk)

        action = "preferencearea.delete_recommendation"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "customer.create"
        producer = [RabbitMQ_User_Producer(queue=queue, exchange=exchange) for queue, exchange in zip(list_queue, list_exchange)]
        try:
            serializer.save()
            for i, service in enumerate(list_services):
                producer[i].publish(message=serializer.data, routing_key=routing_key+action+"_"+service)
                logger.success(f"Success publishing in {routing_key+action + '_' + service}")
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            for p in producer:
                p.close()

        return Response(serializer.data)

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = WorkerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action = "worker.create"
        producer = [RabbitMQ_User_Producer(queue=queue, exchange=exchange) for queue, exchange in zip(list_queue, list_exchange)]
        try:
            serializer.save()
            for i, service in enumerate(list_services):
                producer[i].publish(message=serializer.data, routing_key=routing_key+action+"_"+service)
                logger.success(f"Success publishing in {routing_key+action + '_' + service}")
            
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            for p in producer:
                p.close()

        return Response(serializer.data)

    def update(self, request, pk):
        object = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "worker.update"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            serializer.save()
            service = "recommendation"
            producer.publish(message=serializer.data, routing_key=routing_key + action + '_' + service)
            logger.success(f"Success publishing in {routing_key + action + '_' + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def partial_update(self, request, pk):
        object = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(instance=object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        action = "worker.partialupdate"
        queue = "user_recommendation_queue"
        exchange = "user_recommendation_events"
        producer = RabbitMQ_User_Producer(queue=queue, exchange=exchange)
        try:
            serializer.save()
            service = "recommendation"
            producer.publish(message=serializer.data, routing_key=routing_key + action +"_"+ service)
            logger.success(f"Success publishing in {routing_key + action + '_' + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)