from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('profile/person',PersonViewSet)
router.register('profile/customer',CustomerViewSet)
router.register('profile/worker',WorkerViewSet)
router.register('profile/me',MeViewSet, basename="me")
router.register('profile/user',UserViewSet)
router.register('utils/services',ServicesProvidedViewSet)
router.register('utils/preference-area',PreferenceAreaViewSet)
router.register('utils/experience',ExperienceViewSet)
