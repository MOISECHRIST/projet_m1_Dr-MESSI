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
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
import random

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

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    #permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        raise MethodNotAllowed("PUT", detail="Cette action n'est pas autorisée.")

    def partial_update(self, request, pk=None):
        raise MethodNotAllowed("PATCH", detail="Cette action n'est pas autorisée.")

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
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ServicesProvidedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "servicesprovided.create"
        list_queue2 = ["user_offre_queue", "user_recommendation_queue"]
        list_services2 = [ "offre", "recommendation"]
        list_exchange2 = ["user_offre_events", "user_recommendation_events"]
        producer = [RabbitMQ_User_Producer(queue=queue, exchange=exchange) for queue, exchange in
                    zip(list_queue2, list_exchange2)]

        try:
            serializer.save()
            for i, service in enumerate(list_services2):
                producer[i].publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
                logger.success(f"Success publishing in {routing_key + action + '_' + service}")
        except Exception as e :
            logger.error(f"Error publishing in {routing_key+action} : {e}")
        finally:
            for p in producer:
                p.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = ServicesProvided.objects.get(id=pk)

        action = "servicesprovided.delete"
        list_queue2 = ["user_offre_queue", "user_recommendation_queue"]
        list_services2 = ["offre", "recommendation"]
        list_exchange2 = ["user_offre_events", "user_recommendation_events"]
        producer = [RabbitMQ_User_Producer(queue=queue, exchange=exchange) for queue, exchange in
                    zip(list_queue2, list_exchange2)]
        try:
            object.delete()
            for i, service in enumerate(list_services2):
                producer[i].publish(message=pk, routing_key=routing_key + action + "_" + service)
                logger.success(f"Success publishing in {routing_key + action + '_' + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            for p in producer:
                p.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

class PreferenceAreaViewSet(viewsets.ModelViewSet):
    queryset = PreferenceArea.objects.all()
    serializer_class = PreferenceAreaSerializer
    #permission_classes = [IsAuthenticated]

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
    #permission_classes = [IsAuthenticated]

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
    #permission_classes = [IsAuthenticated]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    #permission_classes = [IsAuthenticated]

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


class MultipleQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = MultipleQuestionAnswer.objects.all()
    serializer_class = MultipleQuestionAnswerSerializer
    #permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=['post'],
        url_path='choice-questions',
        serializer_class=EmptySerializer
    )
    def random_choice_question(self, request, service_id=None):
        try:
            service = ServicesProvided.objects.get(id=service_id)
        except ServicesProvided.DoesNotExist:
            return Response({"error": "Service not found"}, status=404)

        all_service_questions = list(MultipleQuestionAnswer.objects.filter(service=service))
        selected_questions = random.sample(all_service_questions, 5)
        serializer = MultipleQuestionAnswerSerializer(selected_questions, many=True)
        return Response(serializer.data)



class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    #permission_classes = [IsAuthenticated]

class EvaluationAnswerViewSet(viewsets.ModelViewSet):
    queryset = EvaluationAnswer.objects.all()
    serializer_class = EvaluationAnswerSerializer
    #permission_classes = [IsAuthenticated]
