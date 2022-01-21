import uuid
import os

from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
    category = models.ForeignKey(
        'category.Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products"
    )

