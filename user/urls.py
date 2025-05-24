from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('person',PersonViewSet)
router.register('customer',CustomerViewSet)
router.register('worker',WorkerViewSet)
#router.register('me',MeViewSet, basename="me")
router.register('user',UserViewSet)
router.register('services',ServicesProvidedViewSet)
router.register('preference-area',PreferenceAreaViewSet)
router.register('experience',ExperienceViewSet)
