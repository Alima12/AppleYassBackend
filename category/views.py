from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from utils.base_permissions import IsAdminOrReadOnly, AdminRequired
from .serializers import CategorySerializer
from product.serializers import ProductSerializer
from .models.category import Category
from rest_framework.permissions import IsAuthenticated


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    lookup_field = "id"


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetProductsByCategoryView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        category = Category.objects.get(name=name)
        return category.products.all()


class CategoryByNameView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "name"
