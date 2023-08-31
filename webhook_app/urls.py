from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import WebhookViewSet

router = routers.DefaultRouter()
router.register(r'webhooks', WebhookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the router URLs
    # path('webhooks/', include('webhook_app.urls')),  # Include webhook URLs
]

