from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('person',PersonViewSet)
router.register('worker',WorkerViewSet)
router.register('customer',CustomerViewSet)
router.register('post',PublicationViewSet)
router.register('comment',CommentViewSet)
router.register('like',LikeViewSet)
router.register('recommender',RecommenderViewSet)
router.register('print_screen',Screen_PrintViewSet)
