from django import views
from django.db import models
from django.contrib.auth.models import User


class DonarDetails(models.Model):
    name = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=10)
    area = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
