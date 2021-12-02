from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from utils.base_permissions import IsAdminOrReadOnly, AdminRequired
from .serializers import CategorySerializer
from .models.category import Category
from rest_framework.permissions import IsAuthenticated


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    lookup_field = "id"
