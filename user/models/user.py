from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number=None, password=None, email=None):
        if not phone_number:
            raise ValueError("Phone Number Required!")
        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


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
    objects = UserManager()
    REQUIRED_FIELDS = []
