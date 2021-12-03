from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderItem(models.Model):
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name="orders"
    )
    count = models.PositiveIntegerField(
        default=0
    )


class Orders(GeneramModel):
    choices = (
        ("a", "agreed"),
        ("w", "waiting"),
        ("r", "rejected")
    )
    tracking_code = models.CharField(
        max_length=80
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="orders"
    )
    products = models.ManyToManyField(
        OrderItem,
        blank=False,
        related_name="parentOrder"
    )
    status = models.CharField(
        choices=choices,
        max_length=1
    )





