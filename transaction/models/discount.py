from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Discount(GeneramModel):
    title = models.CharField(
        max_length=200
    )
    code = models.CharField(
        max_length=20,
        unique=True
    )
    products = models.ManyToManyField(
        "product.Color",
        blank=True,
        related_name="discounts"
    )
    percent = models.PositiveIntegerField(
        default=10
    )
    max_price = models.PositiveIntegerField(
        default=50000
    )
    customers = models.ManyToManyField(
        User,
        blank=True,
        related_name="used_discounts"
    )
    period = models.DateTimeField(
        default=timezone.now
    )
    reUseAble = models.BooleanField(
        default=False
    )
    just_for = models.ManyToManyField(
        User,
        blank=True,
        related_name="special_discount"
    )

    def is_active(self):
        if self.period > timezone.now():
            return True
        return False

    def is_used(self, user):
        if user not in self.customers.all():
            return True
        return False

    def can_i_use(self, user):
        if (self.is_used(user) or self.reUseAble) and self.is_active():
            return True
        return False



