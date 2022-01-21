from django.db import models
from utils.general_model import GeneramModel
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"settings/", filename)


class Certifications(GeneramModel):
    image = models.ImageField(
        upload_to=get_file_path
    )
    title = models.CharField(
        max_length=50
    )


class WebTitles(GeneramModel):
    browser_title = models.CharField(
        max_length=20
    )
    seo_key_words = models.TextField(

    )
    contact_us = models.CharField(
        max_length=100
    )
    logo = models.ImageField(
        upload_to=get_file_path
    )
    web_name = models.CharField(
        max_length=20
    )
    about_us = models.TextField(

    )
    copy_rights = models.CharField(
        max_length=50
    )
    our_address = models.TextField(
        null=True
    )
