from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('profile/person',PersonViewSet)
router.register('profile/worker',WorkerViewSet)
router.register('profile/customer',CustomerViewSet)
router.register('publication/post',PublicationViewSet)
router.register('publication/comment',CommentViewSet)
router.register('publication/like',LikeViewSet)
router.register('publication/recommender',RecommenderViewSet)

