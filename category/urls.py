from django.urls import path
from .views import CategoryListView, CategoryDetailView


urlpatterns = [
    path("", CategoryListView.as_view(), name="category-list-create"),
    path("<int:id>/", CategoryDetailView.as_view(), name="category-detail"),

]