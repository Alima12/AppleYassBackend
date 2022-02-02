from .serializers import SlidesSerializer, WebTitlesSerializer, CertificatesSerializer, SuperOfferSerializer
from .models import SlideImages, WebTitles, Certifications, SuperOffer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from utils.base_permissions import AdminRequired
from rest_framework.permissions import IsAuthenticated


class SlideListCreateView(ListCreateAPIView):
    serializer_class = SlidesSerializer
    permission_classes = [IsAuthenticated, AdminRequired]

    def get_queryset(self):
        return SlideImages.objects.all()


class SlideListApiView(ListAPIView):
    serializer_class = SlidesSerializer

    def get_queryset(self):
        items = SlideImages.objects.all()
        result = []
        for item in items:
            if item.is_active:
                result.append(item)
        return result

@api_view(['POST'])
def reverse_state(request, id):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})

    slide = get_object_or_404(SlideImages, id=id)
    slide.is_active = not slide.is_active
    slide.save()
    return Response({
        "msg": "Successfully",
        "state": slide.is_active
    })

@api_view(['DELETE'])
def delete(request, id):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})

    slide = get_object_or_404(SlideImages, id=id)
    slide.delete()
    return Response(status=204)


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
