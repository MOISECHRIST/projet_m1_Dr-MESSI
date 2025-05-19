from rest_framework import viewsets, status
from .models import *
from .producer import Producer
from .serializers import *
from rest_framework.response import Response
from loguru import logger
import sys



# Create your views here.
logger.remove()
logger.add(f"logs_warning.log",
           level="WARNING",
           rotation="500mb")

logger.add(sys.stderr, level="SUCCESS")
logger.add(sys.stderr, level="WARNING")

routing_key = "abonnement."
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # permission_classes = [IsPersonLoggedIn]


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    #permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    #permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "subscription.create_recommendation"
        producer = Producer()
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
        object = Subscription.objects.get(id=pk)

        action = "subscription.delete_recommendation"
        producer = Producer()
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action)
            logger.success(f"Success publishing in {routing_key + action}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionRecommendationViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionRecommendation.objects.all()
    serializer_class = SubscriptionRecommendationSerializer
    #permission_classes = [IsAuthenticated]