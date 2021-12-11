from rest_framework import serializers
from .models import Product, Color
from rest_framework.validators import UniqueValidator


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "code",
            "colors",
            "created_at",
            "updated_at",
            "title",
            "name",
            "guarantee",
            "is_super_offer",
            "is_special_offer",
            "is_new",
            "is_hot",
            "category",
            "images",
            "attributes",
            "technical",
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
        return attrs

    def create(self, validated_data):
        product = Product.objects.create(
            code=validated_data['code'],
            title=validated_data['title'],
            name=validated_data['name'],
            detail=validated_data['detail'],
            guarantee=validated_data['guarantee']
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


class ColorSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = Color
        fields = ["id", "inventory", "price", "color", "product","product_code"]

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
