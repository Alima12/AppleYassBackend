from django.db import models
from django.contrib.auth import get_user_model
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"user/{instance.pk}/", filename)


User = get_user_model()


class Images(models.Model):
    image = models.ImageField(
        upload_to= get_file_path,
        default="default_user_image.jpg",
    )
    owner = models.ForeignKey(
        User,
        related_name="images",
        on_delete=models.CASCADE
    )