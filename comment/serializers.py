from rest_framework import serializers
from .models.comments import Comments
from django.contrib.auth import get_user_model
from user.models import Images
from transaction.serializers import SimpleProductSerializer
user = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["image"]


class OwnerSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    username = serializers.CharField()
    images = ImageSerializer(many=True)


class CommentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False, write_only=True)
    product_id = serializers.IntegerField(required=True, write_only=True)
    owner = OwnerSerializer()
    product = SimpleProductSerializer()

    class Meta:
        model = Comments
        fields = "__all__"

    def validate(self, attrs):
        if "parent_id" in attrs.keys():
            attrs["parent"] = Comments.objects.get(id=attrs["parent_id"])
        attrs["owner"] = self.context['request'].user
        return attrs


class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = "__all__"





