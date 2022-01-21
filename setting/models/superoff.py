from django.db import models
from utils.general_model import GeneramModel
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
import os

User = get_user_model()


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(f"supper-offer/", filename)


class SuperOffer(GeneramModel):

    title = models.CharField(
        max_length=20
    )
    image = models.ImageField(
        upload_to=get_file_path
    )
    percent = models.PositiveIntegerField(
        default=30
    )
    percent_image = models.ImageField(
        upload_to=get_file_path
    )
    product = models.ForeignKey(
        "product.Color",
        related_name="is_super_offer",
        on_delete=models.CASCADE
    )
    customers = models.ManyToManyField(
        User,
        related_name="super_offer_used"
    )
    limited = models.BooleanField(
        default=1
    )
    till = models.DateTimeField(
        default=datetime.now
    )
    transaction = models.ManyToManyField(
        "transaction.Transaction",
        related_name="forSuperOffer",
        null=True,
        blank=True
    )

    def is_active(self):
        if self.till > datetime.now():
            return True
        return False

    def how_many_used(self):
        return self.customers.count() or 0

    def can_i_use(self, user):
        if self.limited is False:
            return True
        elif user not in self.customers.all():
            return True
        else:
            return False



