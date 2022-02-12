from .serializers import (
    ProductSerializer,
    CreateProductSerializer,
    ColorSerializer,
    ImageSerializer,
    SimpleColorSerializer,
    AttrSerializer,
    TechSerializer,
)

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveAPIView
)
from .models import Product, Color, ProductImages, TechnicalAttributes, ProductAttributes
from .permission import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.base_permissions import AdminRequired
from rest_framework.response import Response
from .pagination import ProductPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


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


class UpdateProductView(UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    queryset = Product.objects.all()
    lookup_field = "code"


@api_view(['POST', "DELETE"])
def AddImage(request, code, id=None):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    product = get_object_or_404(Product, code=code)
    if request.method == "POST":
        data = request.FILES
        image = ProductImages.objects.create(
            image=data["image"],
            product=product
        )
        image.save()
        images = ImageSerializer(image)
        return Response(images.data, status=201)
    if request.method == "DELETE":
        image = get_object_or_404(ProductImages, id=id)
        image.delete()
        return Response(status=204)


class CreateColorView(ListCreateAPIView):
    serializer_class = ColorSerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    queryset = Color.objects.all()


class UpdateColorView(UpdateAPIView):
    serializer_class = SimpleColorSerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    queryset = Color.objects.all()
    lookup_field = "id"


class GetColorWithId(RetrieveAPIView):
    queryset = Color.objects.all()
    serializer_class = SimpleColorSerializer
    lookup_field = "id"


class GetColorView(APIView):
    serializer_class = ColorSerializer

    def get(self, request, code):
        colors = Color.objects.filter(product__code=code)
        response = ColorSerializer(colors, many=True)
        return Response(
            response.data
        )


@api_view(['POST', "DELETE"])
def SetColor(request, code, id=None):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    product = get_object_or_404(Product, code=code)
    if request.method == "POST":
        color = Color.objects.create(product=product)
        data = request.POST
        if "price" in data.keys():
            color.price = data["price"]
        if "inventory" in data.keys():
            color.inventory = data["inventory"]
        if "color" in data.keys():
            color.color = data["color"]
        color.save()
        data = SimpleColorSerializer(color)
        return Response(data.data, status=201)
    if request.method == "DELETE":
        color = get_object_or_404(Color, id=id)
        color.delete()
        return Response(status=204)


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
    pagination_class = ProductPagination
    filterset_fields = ['category__name', ]
    search_fields = ["title", "name"]

    def get_queryset(self):
        products = Product.objects.all()
        args = self.request.query_params.get("available")
        if args == "true" or args == "0":
            for product in products:
                count = 0
                for color in product.colors.all():
                    count += color.inventory
                if count <= 0:
                    products = products.exclude(id=product.id)

        return products


class UpdateTechView(UpdateAPIView):
    serializer_class = TechSerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    queryset = TechnicalAttributes.objects.all()
    lookup_field = "id"


@api_view(['POST', "DELETE"])
def manage_tech(request, code, id=None):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    product = get_object_or_404(Product, code=code)
    if request.method == "POST":
        data = request.POST
        tech = TechnicalAttributes.objects.create(product=product)
        if "name" in data.keys():
            tech.name = data["name"]
        if "text" in data.keys():
            tech.text = data["text"]
        tech.save()
        data = TechSerializer(tech)
        return Response(data.data, status=201)
    if request.method == "DELETE":
        tech = get_object_or_404(TechnicalAttributes, id=id)
        tech.delete()
        return Response(status=204)


class UpdateAttrView(UpdateAPIView):
    serializer_class = AttrSerializer
    permission_classes = (IsAuthenticated, AdminRequired)
    queryset = ProductAttributes.objects.all()
    lookup_field = "id"


@api_view(['POST', "DELETE"])
def manage_attributes(request, code, id=None):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    product = get_object_or_404(Product, code=code)
    if request.method == "POST":
        data = request.POST
        attr = ProductAttributes.objects.create(product=product)
        if "text" in data.keys():
            attr.text = data["text"]
        attr.save()
        data = AttrSerializer(attr)
        return Response(data.data, status=201)
    if request.method == "DELETE":
        attr = get_object_or_404(ProductAttributes, id=id)
        attr.delete()
        return Response(status=204)
