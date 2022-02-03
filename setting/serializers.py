from rest_framework import serializers
from .models import SlideImages, WebTitles, Certifications, SuperOffer


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

    class Meta:
        model = SuperOffer
        fields = ["id", "title", "image", "percent", "percent_image", "till", "product", "real_price", "total_price"]
        depth = 2
