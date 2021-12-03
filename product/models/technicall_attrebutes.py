from django.db import models


class TechnicalAttributes(models.Model):
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name="technical"
    )
    name = models.CharField(
        max_length=50
    )
    text = models.TextField()

