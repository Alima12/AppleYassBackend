from django.urls import path
from .views import UserListView, UserDetailView, ProfileView, RegisterUser

urlpatterns = [
    path('', UserListView.as_view(), name="users-list"),
    path('<int:pk>/', UserDetailView.as_view(),name="user-detail"),
    path('getMe/', ProfileView.as_view(), name="get-my-info"),
    path("register/", RegisterUser.as_view(), name="register-user"),

]