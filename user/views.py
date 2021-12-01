from .serializers import UserSerializer, RegisterSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.contrib.auth import get_user_model
from utils.base_permissions import AdminRequired, IsNotAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


User = get_user_model()


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminRequired]


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminRequired]


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return user


class RegisterUser(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]
