from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import User

class MeViewSet(viewsets.ViewSet):
    #permission_classes = (IsAuthenticated,)
    def list(self, request):
        user=User.objects.get(username=request.user)
        user_data=UserSerializer(user).data
        return Response(user_data)

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ServicesProvidedViewSet(viewsets.ModelViewSet):
    queryset = ServicesProvided.objects.all()
    serializer_class = ServicesProvidedSerializer

class PreferenceAreaViewSet(viewsets.ModelViewSet):
    queryset = PreferenceArea.objects.all()
    serializer_class = PreferenceAreaSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer