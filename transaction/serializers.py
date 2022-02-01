from rest_framework import serializers
from .models import Orders, Transaction, OrderItem, Discount
from product.models import Color, Product

from rest_framework.validators import UniqueValidator
import uuid
from user.models import Images
from user.serializers import AddressSerializer


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["images", "code", "name", "title"]
        depth = 1


class SimpleColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["price", "color"]
        depth = 1

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
    address = AddressSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    customer = OwnerSerializer()

    class Meta:
        model = Orders
        fields = "__all__"
        # depth = 1


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        depth = 1


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"
        depth = 1


class ManageOrdersSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(
        default=1,
        write_only=True
    )
    color_id = serializers.CharField(
        required=True,
        write_only=True
    )
    status = serializers.CharField(
        read_only=True
    )
    refer_code = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Orders
        exclude = ["customer"]
        depth = 3


    def validate(self, attrs):
        color_id = int(attrs["color_id"])
        product = Color.objects.get(id=color_id)
        attrs["color_id"] = product
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        order = Orders.objects.filter(status="p", customer=user)
        if order.count() > 0:
            order = order[0]
        else:
            order = Orders.objects.create(
                customer=user,
                refer_code=uuid.uuid4().hex[:20].upper(),
            )
        color = validated_data['color_id']
        added = False
        for item in order.items.all():
            if item.product == color:
                item.count += validated_data["count"]
                item.save()
                added = True
        if not added:
            order_item = OrderItem.objects.create(
                product=color,
                count=validated_data["count"],
                price=color.price,
            )
            order_item.save()
            order.items.add(order_item)

        order.calc_discount()
        order.save()
        return order


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["id", "title", "code", "percent", "max_price", "reUseAble", "customers", "is_active", "period"]