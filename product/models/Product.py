import uuid
import os

from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"product/{instance.code}/", filename)


class Product(GeneramModel):
    code = models.CharField(
        max_length=20
    )
    title = models.CharField(
        max_length=200
    )
    name = models.CharField(
        max_length=200
    )
    rate = models.PositiveIntegerField(
    )
    detail = models.TextField(
        verbose_name="Detail"
    )
    guarantee = models.CharField(
        max_length=120
    )
    is_super_offer = models.BooleanField(
        default=False,
    )
    is_special_offer = models.BooleanField(
        default=False,
    )
    is_new = models.BooleanField(
        default=True,
    )
    is_hot = models.BooleanField(
        default=False,
    )
    categtory = models.ForeignKey(
        'category.Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

