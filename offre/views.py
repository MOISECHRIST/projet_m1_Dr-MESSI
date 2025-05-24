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

routing_key = "offre."
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


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = MediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "media.create_recommendation"
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

    def update(self, request, pk):
        object = Media.objects.get(id=pk)
        serializer = MediaSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "media.update_recommendation"
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

    def partial_update(self, request, pk):
        object = Media.objects.get(id=pk)
        serializer = MediaSerializer(instance=object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        action = "media.partialupdate_recommendation"
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
        object = Media.objects.get(id=pk)

        action = "media.delete_recommendation"
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


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "location.create_recommendation"
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

    def update(self, request, pk):
        object = Location.objects.get(id=pk)
        serializer = LocationSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "location.update_recommendation"
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

    def partial_update(self, request, pk):
        object = Location.objects.get(id=pk)
        serializer = LocationSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "location.partialupdate_recommendation"
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
        object = Location.objects.get(id=pk)

        action = "location.delete_recommendation"
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


class WorkOfferViewSet(viewsets.ModelViewSet):
    queryset = WorkOffer.objects.all()
    serializer_class = WorkOfferSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = WorkOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "workoffer.create_recommendation"
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

    def update(self, request, pk):
        object = WorkOffer.objects.get(id=pk)
        serializer = WorkOfferSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "workoffer.update_recommendation"
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

    def partial_update(self, request, pk):
        object = WorkOffer.objects.get(id=pk)
        serializer = WorkOfferSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "workoffer.partialupdate_recommendation"
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
        object = WorkOffer.objects.get(id=pk)

        action = "workoffer.delete_recommendation"
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


class OfferApplicationViewSet(viewsets.ModelViewSet):
    queryset = OfferApplication.objects.all()
    serializer_class = OfferApplicationSerializer
    #permission_classes = [IsAuthenticated]


class RecommenderViewSet(viewsets.ModelViewSet):
    queryset = Recommender.objects.all()
    serializer_class = RecommenderSerializer
    #permission_classes = [IsAuthenticated]