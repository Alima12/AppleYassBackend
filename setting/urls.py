from django.urls import path
from .views import (
    SlideListApiView,
    WebTitlesView,
    CertificateListApiView,
    SuperOfferObjectView,
    reverse_state,
    delete,
    SlideListCreateView,
    EditSlideView,
    CreateCertificateApiView,
    UpdateCertificateApiView,
    UpdateWebTitlesView,
)

name = "Config"

urlpatterns = [
    path("slides/", SlideListApiView.as_view(), name="slide-list"),
    path("slides/list/", SlideListCreateView.as_view(), name="slide-list"),
    path("slides/<int:id>/reverse/", reverse_state, name="reverse-state"),
    path("slides/<int:id>/delete/", delete, name="delete-slide"),
    path("slides/<int:pk>/edit/", EditSlideView.as_view(), name="edit-slide"),


    path("certificates/", CertificateListApiView.as_view(), name="certificates-list"),
    path("certificates/add/", CreateCertificateApiView.as_view(), name="certificates-add"),
    path("certificates/<int:pk>/update/", UpdateCertificateApiView.as_view(), name="certificates-update"),
    path("certificates/<int:pk>/destroy/", UpdateCertificateApiView.as_view(), name="certificates-update"),


    path("setting/<int:pk>/update/", UpdateWebTitlesView.as_view(), name="setting-update"),



    path("super-offer/", SuperOfferObjectView.as_view(), name="get-super-offer"),

    path("", WebTitlesView.as_view(), name="web-title"),
]