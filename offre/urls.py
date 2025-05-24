from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('offer.service/person',PersonViewSet)
router.register('offer.service/customer',CustomerViewSet)
router.register('offer.service/worker',WorkerViewSet)
router.register('offer.service/media',MediaViewSet)
router.register('offer.service/location',LocationViewSet)
router.register('offer.service/work_offer',WorkOfferViewSet)
router.register('offer.service/offer_application',OfferApplicationViewSet)
router.register('offer.service/recommender',RecommenderViewSet)