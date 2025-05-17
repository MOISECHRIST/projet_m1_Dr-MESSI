from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from loguru import logger
import sys
from .producer import Producer


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


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = PublicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "post.create"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def update(self, request, pk):
        object = Publication.objects.get(id=pk)
        serializer = PublicationSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "post.update"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def partial_update(self, request, pk):
        object = Publication.objects.get(id=pk)
        serializer = PublicationSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "post.partialupdate"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = Publication.objects.get(id=pk)

        action = "post.destroy"
        producer = Producer()
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "comment.create"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def update(self, request, pk):
        object = Comment.objects.get(id=pk)
        serializer = CommentSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "comment.update"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def partial_update(self, request, pk):
        object = Comment.objects.get(id=pk)
        serializer = CommentSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "comment.update"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = Comment.objects.get(id=pk)

        action = "comment.destroy"
        producer = Producer()
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "like.create"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def update(self, request, pk):
        object = Like.objects.get(id=pk)
        serializer = LikeSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "like.update"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def partial_update(self, request, pk):
        object = Like.objects.get(id=pk)
        serializer = LikeSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "like.update"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")
        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)

    def destroy(self, request, pk):
        object = Like.objects.get(id=pk)

        action = "like.destroy"
        producer = Producer()
        try:
            object.delete()
            producer.publish(message=pk, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

class RecommenderViewSet(viewsets.ModelViewSet):
    queryset = Recommender.objects.all()
    serializer_class = RecommenderSerializer
    #permission_classes = [IsAuthenticated]


class Screen_PrintViewSet(viewsets.ModelViewSet):
    queryset = Screen_Print.objects.all()
    serializer_class = Screen_PrintSerializer

    def create(self, request):
        serializer = Screen_PrintSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = "screen_view.create"
        producer = Producer()
        try:
            serializer.save()
            producer.publish(message=serializer.data, routing_key=routing_key + action + "_" + service)
            logger.success(f"Success publishing in {routing_key + action + "_" + service}")

        except Exception as e:
            logger.error(f"Error publishing in {routing_key + action+ "_" + service} : {e}")
        finally:
            producer.close()

        return Response(serializer.data)