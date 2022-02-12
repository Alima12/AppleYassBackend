from rest_framework import serializers
from .models import Product, Color, ProductImages, ProductAttributes, TechnicalAttributes
from category.models import Category
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404


class TechSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    text = serializers.CharField(required=False)

    class Meta:
        model = TechnicalAttributes
        fields = "__all__"


class AttrSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False)

    class Meta:
        model = ProductAttributes
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = Color
        fields = ["id", "inventory", "get_price", "color", "product", "product_code", "is_super_offer"]
        depth = 1

    def validate(self, attrs):
        if 'price' not in attrs.keys():
            attrs["price"] = 100000

        if 'inventory' not in attrs.keys():
            attrs["inventory"] = 1

        if "product_code" in attrs.keys():
            attrs["product"] = Product.objects.get(code=attrs["product_code"])

        return attrs

    def create(self, validated_data):
        color = Color.objects.create(
            product=validated_data["product"],
            color=validated_data["color"],
        )
        color.price = validated_data["price"]
        color.inventory = validated_data["inventory"]
        color.save()
        return color


class SimpleProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "images", "code", "name", "title"]


class SimpleColorSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(required=False)
    inventory = serializers.IntegerField(required=False)
    color = serializers.CharField(required=False)
    product = SimpleProductSerializer(required=False)

    class Meta:
        model = Color
        fields = ["id", "price", "inventory", "color", "product"]


class ProductSerializer(serializers.ModelSerializer):
    colors = SimpleColorSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    category_id = serializers.CharField(
        max_length=50,
        write_only=True,
        required=False
    )

    def validate(self, attrs):
        if "category_id" in attrs.keys():
            category = get_object_or_404(Category, id=attrs["category_id"])
            attrs["category"] = category
        return attrs

    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "title",
            "name",
            "colors",
            "guarantee",
            "is_super_offer",
            "is_special_offer",
            "is_new",
            "is_hot",
            "category",
            "category_id",
            "images",
            "attributes",
            "technical",
            "detail",
            "rate"
        ]
        depth = 1


class CreateProductSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=20,
        required=True,
        validators=[UniqueValidator(queryset=Product.objects.all(), message="محصولی با این کد موجود هست")],
    )
    title = serializers.CharField(
        max_length=50,
        required=True
    )
    name = serializers.CharField(
        max_length=50,
        required=True
    )
    category_id = serializers.CharField(
        max_length=50,
        write_only=True,
        required=False
    )
    detail = serializers.CharField(
        required=True
    )
    guarantee = serializers.CharField(
        max_length=50
    )
    is_super_offer = serializers.BooleanField(
        default=False
    )
    is_special_offer = serializers.BooleanField(
        default=False
    )
    is_new = serializers.BooleanField(
        default=True
    )
    is_hot = serializers.BooleanField(
        default=False
    )

    def validate(self, attrs):
        if "category_id" in attrs.keys():
            category = get_object_or_404(Category, id=attrs["category_id"])
            attrs["category"] = category
        return attrs

    def create(self, validated_data):
        product = Product.objects.create(
            code=validated_data['code'],
            title=validated_data['title'],
            name=validated_data['name'],
            detail=validated_data['detail'],
            guarantee=validated_data['guarantee'],
            category=validated_data['category'],
        )
        if 'is_super_offer' in validated_data.keys():
            product.is_super_offer = validated_data['is_super_offer']

        if 'is_special_offer' in validated_data.keys():
            product.is_special_offer = validated_data['is_special_offer']

        if 'is_new' in validated_data.keys():
            product.is_new = validated_data['is_new']

        if 'is_hot' in validated_data.keys():
            product.is_hot = validated_data['is_hot']

        product.save()

        return product


