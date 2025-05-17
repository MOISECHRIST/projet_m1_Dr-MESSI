from rest_framework import viewsets, status
from .models import *
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

service = "recommendation"
routing_key = "publication."
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


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    #permission_classes = [IsAuthenticated]


class WorkOfferViewSet(viewsets.ModelViewSet):
    queryset = WorkOffer.objects.all()
    serializer_class = WorkOfferSerializer
    #permission_classes = [IsAuthenticated]


class OfferApplicationViewSet(viewsets.ModelViewSet):
    queryset = OfferApplication.objects.all()
    serializer_class = OfferApplicationSerializer
    #permission_classes = [IsAuthenticated]