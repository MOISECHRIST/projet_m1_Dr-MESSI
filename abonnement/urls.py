from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('person',PersonViewSet)
router.register('customer',CustomerViewSet)
router.register('worker',WorkerViewSet)
router.register('subscriptions',SubscriptionViewSet)
router.register('recommendation',SubscriptionRecommendationViewSet)