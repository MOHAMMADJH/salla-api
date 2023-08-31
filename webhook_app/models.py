from django.db import models

# Create your models here.
from django.db import models


class Webhook(models.Model):
    # Define fields for webhook data
    name = models.CharField(max_length=100)
    event = models.CharField(max_length=100)
    version = models.IntegerField()
    rule = models.CharField(max_length=200)
    url = models.URLField()
    security_strategy = models.CharField(max_length=50)
    secret = models.CharField(max_length=100)

    def __str__(self):
        return self.name
