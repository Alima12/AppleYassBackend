from django.urls import path
from .views import SlideListApiView, WebTitlesView, CertificateListApiView, SuperOfferObjectView

name = "Config"

urlpatterns = [
    path("slides/", SlideListApiView.as_view(), name="slide-list"),
    path("certificates/", CertificateListApiView.as_view(), name="certificates-list"),
    path("super-offer/", SuperOfferObjectView.as_view(), name="get-super-offer"),

    path("", WebTitlesView.as_view(), name="web-title"),
]