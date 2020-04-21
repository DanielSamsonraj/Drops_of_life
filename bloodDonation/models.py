from django import views
from django.db import models


class donarDetails(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    pasword = models.CharField(max_length=8)
    blood_group = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=10)
    area = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
