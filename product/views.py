from .serializers import ProductSerializer, CreateProductSerializer, ColorSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from .models import Product, Color, ProductImages
from .permission import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.base_permissions import AdminRequired
from rest_framework.response import Response
from .pagination import ProductPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters


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


class GetColorView(APIView):
    serializer_class = ColorSerializer

    def get(self, request, code):
        colors = Color.objects.filter(product__code=code)
        response = ColorSerializer(colors, many=True)
        return Response(
            response.data
        )


class GetNewProducts(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        response = []
        result = Product.objects.all().order_by("-updated_at")
        for item in result:
            if item.is_new:
                response.append(item)

        return response[:5]


class GetHotProducts(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        response = []
        result = Product.objects.all().order_by("-updated_at")
        for item in result:
            if item.is_hot:
                response.append(item)

        return response[:5]


class RelatedProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        code = self.kwargs["code"]
        product = get_object_or_404(Product, code=code)
        result = Product.objects.filter(
            Q(category=product.category)
        ).exclude(code=code)
        return result


class FilterProducts(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    filterset_fields = ['category__name', ]
    search_fields = ["title", "name"]
