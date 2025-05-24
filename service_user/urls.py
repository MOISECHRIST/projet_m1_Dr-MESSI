from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from user.urls import router as user_router
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from decouple import config

shema_view = get_schema_view(
    openapi.Info(
        title = "User service API",
        default_version = 'v1.0',
        description = "This API allow you to manage users data (create user, edit user information, add more features like experience and service provided for workers or preference for any users)",
        contact = openapi.Contact(email=config("AUTHOR_EMAIL"), name = config("AUTHOR_NAME"), url=config("AUTHOR_URL"))
    ),
    public = True,
    permission_classes = (permissions.AllowAny,)
)

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user.service/', include(router.urls)),
    path("swagger/", shema_view.with_ui('swagger', cache_timeout = 0), name='schema_swagger-ui'),
    path("redoc/", shema_view.with_ui('redoc', cache_timeout = 0), name='schema_redoc'),
    path("swagger.json", shema_view.without_ui(cache_timeout = 0), name='schema_json'),
    path('user.service/auth/', include('dj_rest_auth.urls'))
]
