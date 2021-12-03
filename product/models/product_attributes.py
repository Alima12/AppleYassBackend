from django.db import models


class ProductAttributes(models.Model):
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name="attributes"
    )
    text = models.TextField()

