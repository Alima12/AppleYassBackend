from django.urls import path
from .views import (
    CommentsListView,
    GetCommentsByProductView,
    like,
    dislike,
    AddCommentView,

)


urlpatterns = [
    path("", CommentsListView.as_view(), name="comments-list"),
    path("<str:product_code>/", GetCommentsByProductView.as_view(), name="product-comments"),
    path("<str:code>/like/", like, name="like-comment"),
    path("<str:code>/dislike/", dislike, name="dislike-comment"),
    path("add/<str:product_code>/", AddCommentView.as_view(), name="add-comment"),

]