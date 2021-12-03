from django.urls import path
from .views import ProductListView, ProductDetailView, CreateProductView

urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
    path('<str:code>/', ProductDetailView.as_view(), name="product-detail"),
    path('product/create/', CreateProductView.as_view(), name="create-product"),

]