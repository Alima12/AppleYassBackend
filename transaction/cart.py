from datetime import datetime
from models.cart import Cart


class MyCart:
    items = list()
    last_update = datetime()
    discount = None
    owner = None
    discount_amount = 0
    state = "empty"

    def __init__(self, user):
        self.cart = Cart.objects.get(owner=user)


    def add(self, cart_item):
        self.items.append(cart_item)

    def remove(self, product):
        self.items = [item for item in self.items if item.code != product]
        return

    def remove_all(self):
        self.items = list()

    def get_count(self):
        count = 0
        for item in self.items:
            count += item.quantity
        return count

    def get_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item.unit_price * item.quantity
        if self.discount is not None:
            total_price = self.set_discount(total_price)
        return total_price

    def set_discount(self, price):
        if not self.discount.is_active():
            return price
        if self.discount.is_used(self.owner) and not self.discount.reUseAble:
            return price

        self.discount_amount = (price * self.discount.percent) / 100
        price -= self.discount_amount

        return price

    def change_state(self, status):
        self.state = status






