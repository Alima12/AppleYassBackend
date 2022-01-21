from django.db import models
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"category/", filename)


class Category(models.Model):
    name = models.CharField(
        max_length=20,
    )
    title = models.CharField(
        max_length=50,
    )
    image = models.ImageField(
        upload_to=get_file_path,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    def __str__(self):
        return f"{self.title}({self.name})"