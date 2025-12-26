# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.
class Profiling(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=23, blank=False, null=False)
    password = models.CharField(max_length=23, blank=False, null=False)
    email = models.CharField(max_length=34, blank=False)

    def __str__(self):
        return f"{self.username}"