from rest_framework import serializers
from .models import Orders, Transaction, OrderItem, Discount
from product.models import Color
from rest_framework.validators import UniqueValidator
import uuid


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
        depth = 3


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


class ManageOrdersSerializer(serializers.Serializer):
    count = serializers.IntegerField(
        default=1
    )
    color_id = serializers.CharField(
        required=True,
        write_only=True
    )

    def validate(self, attrs):
        color_id = int(attrs["color_id"])
        product = Color.objects.get(id=color_id)
        attrs["color_id"] = product
        return attrs

    def create(self, validated_data):
        color = validated_data['color_id']
        order_item = OrderItem.objects.create(
            product=color,
            count=validated_data["count"],
            price=color.price,
        )
        order_item.save()
        user = self.context['request'].user
        order = Orders.objects.filter(status="p", customer=user)
        if order.count() > 0:
            order = order[0]
            order.items.add(order_item)
        else:
            order = Orders.objects.create(
                customer=user,
                refer_code=uuid.uuid4().hex[:20].upper(),
            )
            order.items.add(order_item)
        order.save()
        return color


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["id", "title", "code", "percent", "max_price", "reUseAble", "customers", "is_active", "period"]