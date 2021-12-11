from .serializers import ProductSerializer, CreateProductSerializer, ColorSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from .models import Product, Color, ProductImages
from .permission import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.base_permissions import AdminRequired
from rest_framework.response import Response
from .pagination import ProductPagination


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'code'


def set_product_image(product, files):
    images = []
    product = Product.objects.get(code=product["code"])
    for item in files:
        item = files[item]
        image = ProductImages.objects.create(
            product=product,
            image=item
        )
        image.save()
        images.append(image)
    return images


class CreateProductView(APIView):
    serializer_class = CreateProductSerializer
    permission_classes = (IsAuthenticated, AdminRequired)

    def post(self, request):
        product = CreateProductSerializer(data=request.POST)
        if product.is_valid():
            product.save()
            files = request.FILES
            set_product_image(product.data, files)
            return Response(product.data, status=201)
        else:
            return Response(product.errors, status=400)


class CreateColorView(ListCreateAPIView):
    serializer_class = ColorSerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    queryset = Color.objects.all()


