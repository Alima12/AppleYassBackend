from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=20,
    )
    title = models.CharField(
        max_length=50,
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.title}({self.name})"