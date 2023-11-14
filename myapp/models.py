from django.db import models

# Create your models here.

from django.db import models

class KeyValue(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
