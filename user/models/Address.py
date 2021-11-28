from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Address(models.Model):
    city = models.CharField(
        max_length=120
    )
    rest_of = models.TextField(

    )
    owner = models.ForeignKey(
        User,
        related_name="address",
        on_delete=models.CASCADE
    )