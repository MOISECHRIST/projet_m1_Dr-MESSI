from rest_framework import viewsets, status
from .models import *
from .serializers import *
from loguru import logger
import sys
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
logger.remove()
logger.add(f"logs_warning.log",
           level="WARNING",
           rotation="500mb")

logger.add(sys.stderr, level="SUCCESS")
logger.add(sys.stderr, level="WARNING")


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


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    #permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    #permission_classes = [IsAuthenticated]

    def update(self, request, pk):
        raise MethodNotAllowed("PUT", detail="Cette action n'est pas autorisée.")

    def partial_update(self, request, pk):
        raise MethodNotAllowed("PATCH", detail="Cette action n'est pas autorisée.")

    @action(
        detail=True,
        methods=['post'],
        url_path='read-message',
        serializer_class=EmptySerializer
    )
    def read_my_message(self, request, pk=None):
        message = Message.objects.get(id=pk)
        message.message_read()
        message.save()
        return Response(MessageSerializer(data=message).data)

    @action(
        detail=True,
        methods=['post'],
        url_path='receive-message',
        serializer_class=EmptySerializer
    )
    def receive_my_message(self, request, pk=None):
        message = Message.objects.get(id=pk)
        message.message_received()
        message.save()
        return Response(MessageSerializer(data=message).data)