from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Webhook
from .serializers import WebhookSerializer


class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
