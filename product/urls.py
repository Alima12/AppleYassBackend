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
    FilterProducts,
    UpdateProductView,
    AddImage,
    SetColor,
    UpdateColorView,
    UpdateTechView,
    manage_tech,
    manage_attributes,
    UpdateAttrView,
    GetColorWithId,
)

urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
    path('searching/', FilterProducts.as_view(), name="searching"),
    path('<str:code>/', ProductDetailView.as_view(), name="product-detail"),
    path('<str:code>/related/', RelatedProductsView.as_view(), name="related-product"),
    path('<int:id>/color/', GetColorWithId.as_view(), name="get-color"),

    path('<str:code>/colors/', GetColorView.as_view(), name="product-colors"),

    path('product/create/', CreateProductView.as_view(), name="create-product"),
    path('product/update/<str:code>/', UpdateProductView.as_view(), name="update-product"),
    path('product/images/<str:code>/', AddImage, name="add-image"),
    path('product/images/<str:code>/delete/<int:id>/', AddImage, name="add-image"),

    path('product/new/', GetNewProducts.as_view(), name="new-products"),
    path('product/hot/', GetHotProducts.as_view(), name="hot-products"),

    path('product/colors/', CreateColorView.as_view(), name="color-product"),
    path('product/colors/<str:code>/add/', SetColor, name="color-product-add"),
    path('product/colors/<str:code>/delete/<int:id>/', SetColor, name="color-product-delete"),
    path('product/colors/<int:id>/update/', UpdateColorView.as_view(), name="color-product-update"),


    path('product/tech/<str:code>/add/', manage_tech, name="tech-product-add"),
    path('product/tech/<str:code>/delete/<int:id>/', manage_tech, name="tech-product-delete"),
    path('product/tech/<int:id>/update/', UpdateTechView.as_view(), name="tech-product-update"),

    path('product/attr/<str:code>/add/', manage_attributes, name="attr-product-add"),
    path('product/attr/<str:code>/delete/<int:id>/', manage_attributes, name="attr-product-delete"),
    path('product/attr/<int:id>/update/', UpdateAttrView.as_view(), name="attr-product-update"),

]