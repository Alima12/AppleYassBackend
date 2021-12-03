from django.db import models
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"product/{instance.product.code}/", filename)


class ProductImages(models.Model):
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to=get_file_path,
    )
