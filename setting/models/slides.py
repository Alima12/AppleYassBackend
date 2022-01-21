from django.db import models
from utils.general_model import GeneramModel
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"slides/", filename)


class SlideImages(GeneramModel):
    image = models.ImageField(
        upload_to=get_file_path,
    )
    text = models.CharField(
        max_length=30
    )
    is_active = models.BooleanField(
        default=True
    )
    rank = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        ordering = ["rank"]


