from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.urls import router as user_router

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls'))
]
