from utils.general_model import GeneramModel
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderItem(GeneramModel):
    product = models.ForeignKey(
        "product.Color",
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(
        default=1
    )
    price = models.PositiveIntegerField(
        default=0
    )


class Orders(GeneramModel):
    status_choices = (
        ("p", "process"),
        ("c", "checkout"),
        ("a", "accepted"),
        ("s", "send to post"),
        ("d", "delivered"),
        ("r", "returned"),
        ("f", "failed")

    )
    refer_code = models.CharField(
        max_length=60,
        unique=True
    )
    items = models.ManyToManyField(
        OrderItem,
        blank=True,
        related_name="inOrder"
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner"
    )
    discount = models.ForeignKey(
        "transaction.Discount",
        related_name="orders",
        null=True,
        on_delete=models.SET_NULL
    )
    status = models.CharField(
        choices=status_choices,
        max_length=1,
        default="p"
    )
    total_price = models.PositiveIntegerField(
        default=0
    )
    real_price = models.PositiveIntegerField(
        default=0
    )
    address = models.ForeignKey(
        "user.Address",
        related_name="orders",
        null=True,
        on_delete=models.SET_NULL
    )

    def get_total_price(self):
        _price = 0
        for item in self.items.all():
            _price += item.price * item.count
        self.real_price = _price
        return _price

    def calc_discount(self):
        total_price = self.get_total_price()
        discount_amount = 0
        if self.discount is not None:
           if self.discount.is_active():
                percent = self.discount.percent
                discount_amount = (total_price * percent) / 100
        self.total_price = total_price - discount_amount
        self.save()
        return self.total_price

    def get_amount_saved(self):
        return self.real_price - self.total_price






