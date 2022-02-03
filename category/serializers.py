from rest_framework import serializers
from .models.category import Category
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Category.objects.all(), message="نام دسته بندی باید منحصر به فرد باشد")],
        required=True
    )

    class Meta:
        model = Category
        fields = ["id", "parent_id", "name", "title", "image", "parent", "children"]
        depth = 1


    def create(self, validated_data):
        parent = None
        if "parent_id" in validated_data.keys():
            parent = Category.objects.get(id=validated_data["parent_id"])
        image = validated_data["image"] or None
        category = Category.objects.create(
            name=validated_data["name"],
            title=validated_data["title"],
            parent=parent,
            image=image
        )
        category.save()

        return category
