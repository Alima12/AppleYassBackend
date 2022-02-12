from .serializers import CommentSerializer, AddCommentSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from .models.comments import Comments
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.base_permissions import AdminRequired
from product.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser


class CommentsListView(ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class GetCommentsByProductView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_code = self.kwargs["product_code"]
        return Comments.objects.filter(product__code=product_code, status="a")


class AddCommentView(CreateAPIView):
    serializer_class = AddCommentSerializer

    def post(self, request, *args, **kwargs):
        received_data = request.POST
        product = kwargs["product_code"]
        product = get_object_or_404(Product, code=product)
        content = received_data["content"]
        user = request.user
        parent = None
        if "parent_id" in received_data.keys():
            parent = get_object_or_404(Comments, id=int(received_data["parent_id"])) or None

        comment = Comments.objects.create(
            content=content,
            product=product,
            parent=parent,
        )
        if user.is_authenticated:
            comment.owner = user
        comment.save()
        comment = AddCommentSerializer(comment)

        return Response(
            status=201,
            data=comment.data
        )


@api_view(['POST'])
def like(request, code):
    code = request.POST["comment"]
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})

    comment = get_object_or_404(Comments, id=int(code))
    if user not in comment.likes.all():
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        comment.likes.add(user)
    else:
        comment.likes.remove(user)

    comment.save()
    comment = AddCommentSerializer(comment).data
    return Response({
        "likes": comment["likes"],
        "dislikes": comment["dislikes"],
    })


@api_view(['POST'])
def dislike(request, code):
    code = request.POST["comment"]
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})

    comment = get_object_or_404(Comments, id=int(code))
    if user not in comment.dislikes.all():
        if user in comment.likes.all():
            comment.likes.remove(user)
        comment.dislikes.add(user)
    else:
        comment.dislikes.remove(user)

    comment.save()
    comment = AddCommentSerializer(comment).data
    return Response({
        "likes": comment["likes"],
        "dislikes": comment["dislikes"],
    })


@api_view(['POST'])
def accept(request, id):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    comment = get_object_or_404(Comments, id=id)
    comment.status = "a"
    comment.save()
    comment = CommentSerializer(comment)

    return Response(comment.data)


@api_view(['POST'])
def reject(request, id):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    comment = get_object_or_404(Comments, id=id)
    comment.status = "r"
    comment.save()

    return Response(status=204)


@api_view(['DELETE'])
def delete(request, id):
    user = request.user or None
    if user is None:
        return Response({"message": "Who Are You?"})
    if not user.is_admin:
        return Response({"message": "You dont have permission!"})
    comment = get_object_or_404(Comments, id=id)
    comment.delete()
    return Response(status=204)