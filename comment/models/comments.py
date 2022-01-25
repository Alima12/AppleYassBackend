from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Comments(GeneramModel):
    status_choices = (
        ("a", "accepted"),
        ("w", "waited"),
        ("r", "rejected")
    )
    owner = models.ForeignKey(
        User,
        related_name="my_comments",
        null=True,
        on_delete=models.SET_NULL,
        blank=True
    )
    product = models.ForeignKey(
        "product.Product",
        related_name="comments",
        on_delete=models.CASCADE,
        null=False
    )
    content = models.TextField(

    )
    likes = models.ManyToManyField(
        User,
        related_name="liked_comments",
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name="disliked_comments",
        blank=True
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        related_name="children",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=status_choices,
        default="w"
    )

    def get_likes(self):
        return self.likes.count()

    def get_dislikes(self):
        return self.dislikes.count()
