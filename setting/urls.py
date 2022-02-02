from django.urls import path
from .views import (
    SlideListApiView,
    WebTitlesView,
    CertificateListApiView,
    SuperOfferObjectView,
    reverse_state,
    delete,
    SlideListCreateView,
)

name = "Config"

urlpatterns = [
    path("slides/", SlideListApiView.as_view(), name="slide-list"),
    path("slides/list/", SlideListCreateView.as_view(), name="slide-list"),

    path("slides/<int:id>/reverse/", reverse_state, name="reverse-state"),
    path("slides/<int:id>/delete/", delete, name="delete-slide"),

    path("certificates/", CertificateListApiView.as_view(), name="certificates-list"),
    path("super-offer/", SuperOfferObjectView.as_view(), name="get-super-offer"),

    path("", WebTitlesView.as_view(), name="web-title"),
]