from django.shortcuts import render
from .serializers import SlidesSerializer, WebTitlesSerializer, CertificatesSerializer, SuperOfferSerializer
from .models import SlideImages, WebTitles, Certifications, SuperOffer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


class SlideListApiView(ListAPIView):
    queryset = SlideImages.objects.all()
    serializer_class = SlidesSerializer


class CertificateListApiView(ListAPIView):
    queryset = Certifications.objects.all()
    serializer_class = CertificatesSerializer


class WebTitlesView(APIView):
    serializer_class = WebTitlesSerializer

    def get(self, request):
        title = WebTitles.objects.last()
        title = WebTitlesSerializer(title)
        return Response(
            title.data
        )


class SuperOfferObjectView(APIView):
    serializer_class = SuperOfferSerializer

    def set_discount_prices(self, instance):
        instance.real_price = instance.product.price
        instance.total_price = instance.product.get_price(instance)
        return instance


    def get(self, request):
        offer = SuperOffer.objects.last()
        offer = self.set_discount_prices(offer)
        offer = SuperOfferSerializer(offer)
        return Response(
            offer.data
        )
