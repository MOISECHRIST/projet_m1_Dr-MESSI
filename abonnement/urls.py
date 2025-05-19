from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('subscrip/person',PersonViewSet)
router.register('subscrip/customer',CustomerViewSet)
router.register('subscrip/worker',WorkerViewSet)
router.register('subscrip/subscriptions',SubscriptionViewSet)
router.register('subscrip/recommendation',SubscriptionRecommendationViewSet)