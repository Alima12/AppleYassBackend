from django.db import models

class GeneramModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        verbose_name="Updated at"
    )

    class Meta:
        abstract = True