from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        null=False,
    )
    national_code = models.CharField(
        max_length=10,
        null=True
    )
    is_admin = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
