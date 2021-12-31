from django.contrib import admin
from .models import Orders, Transaction, Discount, OrderItem
# Register your models here.


admin.site.register(OrderItem)
admin.site.register(Orders)
admin.site.register(Transaction)
admin.site.register(Discount)

