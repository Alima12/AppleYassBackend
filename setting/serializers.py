from rest_framework import serializers
from .models import SlideImages, WebTitles, Certifications, SuperOffer
from product.models import Color


class SlidesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = SlideImages
        fields = "__all__"


class WebTitlesSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)

    class Meta:
        model = WebTitles
        fields = "__all__"


class CertificatesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    title = serializers.CharField(required=False)

    class Meta:
        model = Certifications
        fields = "__all__"


class SuperOfferSerializer(serializers.ModelSerializer):
    real_price = serializers.IntegerField(read_only=True, default=30000)
    total_price = serializers.IntegerField(read_only=True, default=10000)
    users = serializers.IntegerField(default=0, read_only=True)
    color_id = serializers.IntegerField(write_only=True)
    image = serializers.ImageField(required=False)
    percent_image = serializers.ImageField(required=False)

    class Meta:
        model = SuperOffer
        fields = ["id", "title", "image", "percent", "percent_image", "limited", "till", "product", "real_price", "total_price", "users", "color_id"]
        depth = 2

    def validate(self, attrs):
        if "color_id" in attrs.keys() and attrs["color_id"] is not None:
            attrs["product"] = Color.objects.get(id=attrs["color_id"])
            del attrs["color_id"]
        return attrs

