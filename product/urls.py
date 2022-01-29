from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CreateProductView,
    CreateColorView,
    GetColorView,
    GetNewProducts,
    GetHotProducts,
    RelatedProductsView,
    FilterProducts

)

urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
    path('searching/', FilterProducts.as_view(), name="searching"),
    path('<str:code>/', ProductDetailView.as_view(), name="product-detail"),
    path('<str:code>/related/', RelatedProductsView.as_view(), name="related-product"),

    path('<str:code>/colors/', GetColorView.as_view(), name="product-colors"),

    path('product/create/', CreateProductView.as_view(), name="create-product"),
    path('product/new/', GetNewProducts.as_view(), name="new-products"),
    path('product/hot/', GetHotProducts.as_view(), name="hot-products"),

    path('product/colors/', CreateColorView.as_view(), name="color-product"),


]