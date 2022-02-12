from django.urls import path
from .views import DashboardApiView

urlpatterns = [
    path('', DashboardApiView.as_view(), name="dashboard"),


]




