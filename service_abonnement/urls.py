"""
URL configuration for service_abonnement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from abonnement.urls import router as subscription_router
from decouple import config
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

shema_view = get_schema_view(
    openapi.Info(
        title = "subscription service API",
        default_version = 'v1.0',
        description = "This API allow customers to subscript to workers and follow them latest updates.",
        contact = openapi.Contact(email=config("AUTHOR_EMAIL"), name = config("AUTHOR_NAME"), url=config("AUTHOR_URL"))
    ),
    public = True,
    permission_classes = (permissions.AllowAny,)
)

router = routers.DefaultRouter()
router.registry.extend(subscription_router.registry)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscription.service/', include(router.urls)),
    path("swagger/", shema_view.with_ui('swagger', cache_timeout = 0), name='schema_swagger-ui'),
    path("redoc/", shema_view.with_ui('redoc', cache_timeout = 0), name='schema_redoc'),
    path("swagger.json", shema_view.without_ui(cache_timeout = 0), name='schema_json')
]
