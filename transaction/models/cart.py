from django.db import models
from django.contrib.auth import get_user_model
from utils.general_model import GeneramModel

User = get_user_model()


class CartItem(GeneramModel):
    product = models.ForeignKey(
        "product.Color",
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(
        default=1
    )
    unit_price = models.PositiveIntegerField(
        default=0
    )
    cart = models.ForeignKey(
        'transaction.Cart',
        on_delete=models.CASCADE,
        related_name="items"
    )


class Cart(models.Model):
    status_choices = (
        ("c", "checkout"),
        ("f", "finally"),
        ("n", "normal")
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    discount = models.ForeignKey(
        "transaction.Discount",
        related_name="in_cart",
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.CharField(
        choices=status_choices,
        max_length=1,
        default="n"
    )
    total_price = models.PositiveIntegerField(
        default=0
    )
    real_price = models.PositiveIntegerField(
        default=0
    )
