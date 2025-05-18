from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('offer/person',PersonViewSet)
router.register('offer/customer',CustomerViewSet)
router.register('offer/worker',WorkerViewSet)
router.register('offer/media',MediaViewSet)
router.register('offer/location',LocationViewSet)
router.register('offer/work_offer',WorkOfferViewSet)
router.register('offer/offer_application',OfferApplicationViewSet)
router.register('offer/recommender',RecommenderViewSet)