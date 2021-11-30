from .serializers import ProductSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .models import Product
from .permission import IsAdminOrReadOnly


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'code'





