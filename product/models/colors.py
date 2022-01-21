from utils.general_model import GeneramModel
from django.db import models
from setting.models import SuperOffer
from datetime import datetime


class Color(GeneramModel):
    product = models.ForeignKey(
        'product.Product',
        blank=False,
        on_delete=models.CASCADE,
        null=False,
        related_name="colors"
    )
    price = models.PositiveIntegerField(
        default=0
    )
    inventory = models.PositiveIntegerField(
        default=0
    )
    color = models.CharField(
        max_length=30
    )

    def get_toman_price(self):
        return self.price / 10

    def get_price(self, instance=None):
        super_offer = SuperOffer.objects.filter(product__pk=self.pk, till__gt=datetime.now())
        if super_offer.count() > 0:
            price = int((self.price * super_offer[0].percent) / 100)
            price = self.price - price
        else:
            price = self.price
        return price
