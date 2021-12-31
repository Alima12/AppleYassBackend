from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Transaction(GeneramModel):
    status_choices = (
        ("w", "waited"),
        ("s", "success"),
        ("r", "returned"),
        ("f", "failed")
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    refer_code = models.CharField(
        max_length=60,
        unique=True
    )
    amount = models.PositiveIntegerField(
        default=0
    )
    status = models.CharField(
        max_length=1,
        choices=status_choices
    )
    order = models.ForeignKey(
        "transaction.Orders",
        on_delete=models.CASCADE,
        related_name="transaction"
    )
