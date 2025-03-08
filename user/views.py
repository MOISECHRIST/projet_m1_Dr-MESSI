import sys
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from .RabbitMQ import RabbitMQ_User_Producer
from  loguru import logger



logger.remove()
logger.add(f"logs_warning.log",
           level="WARNING",
           rotation="500mb")

logger.add(sys.stderr, level="SUCCESS")
logger.add(sys.stderr, level="WARNING")
routing_key = "user."

class MeViewSet(viewsets.ViewSet):

    def list(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        try:
            user = User.objects.get(username=request.user.username)  # Utiliser request.user.username
            user_data = UserSerializer(user).data
            return Response(user_data)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ServicesProvidedViewSet(viewsets.ModelViewSet):
    queryset = ServicesProvided.objects.all()
    serializer_class = ServicesProvidedSerializer

    def create(self, request):
        serializer = ServicesProvidedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "servicesprovided.create"
        producer = RabbitMQ_User_Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key+action)
            logger.success(f"Success publishing in {routing_key+action}")
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = ServicesProvided.objects.get(id=pk)

        action = "servicesprovided.delete"
        producer = RabbitMQ_User_Producer()
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

    def create(self, request):
        serializer = PreferenceAreaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "preferencearea.create"
        producer = RabbitMQ_User_Producer()
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

        action = "preferencearea.update"
        producer = RabbitMQ_User_Producer()
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

        action = "preferencearea.partialupdate"
        producer = RabbitMQ_User_Producer()
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

        action = "preferencearea.delete"
        producer = RabbitMQ_User_Producer()
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

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "customer.create"
        producer = RabbitMQ_User_Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key+action)
            logger.success(f"Success publishing in {routing_key+action}")
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = Customer.objects.get(id=pk)

        action = "customer.delete"
        producer = RabbitMQ_User_Producer()
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def create(self, request):
        serializer = WorkerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "worker.create"
        producer = RabbitMQ_User_Producer()
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
        object = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "worker.update"
        producer = RabbitMQ_User_Producer()
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
        object = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(instance=object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        action = "worker.partialupdate"
        producer = RabbitMQ_User_Producer()
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
        object = Worker.objects.get(id=pk)

        action = "worker.delete"
        producer = RabbitMQ_User_Producer()
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)