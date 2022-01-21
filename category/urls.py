from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryListApiView,
    GetProductsByCategoryView,
    CategoryByNameView,
)


urlpatterns = [
    path("", CategoryListView.as_view(), name="category-list-create"),
    path("<int:id>/", CategoryDetailView.as_view(), name="category-detail"),
    path("list/", CategoryListApiView.as_view(), name="category-list"),
    path("<str:name>/", GetProductsByCategoryView.as_view(), name="category-product"),
    path("<str:name>/detail/", CategoryByNameView.as_view(), name="category-name-detail"),

]