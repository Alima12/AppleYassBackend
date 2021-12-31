from django.contrib import admin
from .models import (
    Product,
    ProductImages,
    Color,
    ProductAttributes,
    TechnicalAttributes
)

admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Color)
admin.site.register(ProductAttributes)
admin.site.register(TechnicalAttributes)

