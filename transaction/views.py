from .serializers import (
    OrderSerializer,
    TransactionSerializer,
    ManageOrdersSerializer,
    OrderItemSerializer,
    DiscountSerializer,
    SimpleProductSerializer,
    SimpleColorSerializer,
)
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from .models import Orders, Transaction, OrderItem, Discount
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from utils.base_permissions import AdminRequired
from product.models import Color
from rest_framework.decorators import api_view
from user.models import Address


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, AdminRequired)

    def get_queryset(self):
        return Orders.objects.all().exclude(status__in=["f", "p"])


class MyOrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Orders.objects.filter(customer=user).exclude(status__in=["f", "p"])


class TransactionListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class MyTransactionListView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(customer=user)


class OrderItemView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ManageCart(ListCreateAPIView):
    serializer_class = ManageOrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        order = Orders.objects.filter(customer=self.request.user, status="p")
        order[0].calc_discount()
        return order


class DiscountListCreateView(ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class DiscountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class UpdateOrderItem(APIView):

    def post(self, request):
        user = request.user
        order = Orders.objects.get(customer=user, status="p")
        order.status = "c"
        order.calc_discount()
        order.save()
        order = OrderSerializer(order)
        return Response(
            order.data
        )

    def put(self, request, item):
        user = request.user
        new_value = int(request.POST["new_value"])
        order = get_object_or_404(Orders, customer=user, status="p")
        item = order.items.get(product=get_object_or_404(Color, id=item))
        item.count = new_value
        item.save()
        order.calc_discount()
        response = {
            "msg": "new value combined successfully!",
            "newValue": new_value,
            "new_total_price": order.total_price,
            "new_real_price": order.real_price,
        }
        return Response(response, status=200)


    def delete(self, request, item):
        user = self.request.user
        color = get_object_or_404(Color, id=item)
        order = get_object_or_404(Orders, status="p", customer=user)
        order.items.remove(order.items.get(product=color))
        order.save()

        return Response(status=204)


class DiscountDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        code = request.POST["code"]
        discount = get_object_or_404(Discount, code=code)
        order = Orders.objects.filter(customer=user, discount__code=discount.code).count()
        if discount.is_active() and\
                (order < 1 or discount.reUseAble):
            order = get_object_or_404(Orders, customer=user, status='p')
            order.discount = discount
            discount.customers.add(user)
            discount.save()
            order.calc_discount()
            order.save()
            data = DiscountSerializer(discount)
            msg = data.data
            return Response(msg)
        return Response(data="شما نمیتوانید از این کد تخفیف استفاده کنید", status=403)

    # def get(self, request, code):
    #     user = request.user
    #     discount = get_object_or_404(Discount, code=code)
    #     order = Orders.objects.filter(customer=user, discount__code=discount.code).count()
    #     if not discount.is_active():
    #         msg = "مهلت استفاده از کد تخفیف مورد نظر به اتمام رسیده"
    #     elif order > 0 and not discount.reUseAble:
    #         msg = "شما قبلا از این کد تخفیف استاده کرده اید"
    #     else:
    #         data = DiscountSerializer(discount)
    #         msg = data.data
    #
    #     return Response(
    #         msg
    #     )

    def delete(self, request):
        user = request.user
        code = request.POST["code"]
        discount = get_object_or_404(Discount, code=code)
        order = get_object_or_404(Orders, customer=user, status='p')
        order.discount = None
        discount.customers.remove(user)
        discount.save()
        order.save()
        return Response(
            status=204
        )


class GetMyCheckout(APIView):

    def post(self, request):
        user = request.user
        order = Orders.objects.get(customer=user, status="p")
        order.status = "c"
        order.calc_discount()
        order.save()
        for o in Orders.objects.filter(customer=user, status="c"):
            if o.id != order.id:
                o.status = "f"
                o.save()

        order = OrderSerializer(order)
        return Response(
            order.data
        )

    def get(self, request):
        user = request.user
        order = Orders.objects.get(customer=user, status="c")
        order.calc_discount()
        order = OrderSerializer(order)
        return Response(
            order.data
        )


class ShoppingItems(APIView):

    def get(self, request, refer_code):
        user = request.user
        if user.is_admin:
            order = get_object_or_404(Orders, refer_code=refer_code)
        else:
            order = get_object_or_404(Orders, customer=user, refer_code=refer_code)
        items = []
        colors = []
        counts = []
        for item in order.items.all():
            __item = item.product.product
            colors.append(item.product)
            items.append(__item)
            counts.append(item.count)

        items = SimpleProductSerializer(items, many=True)
        colors = SimpleColorSerializer(colors, many=True)
        msg = {
            "products": items.data,
            "colors": colors.data,
            "counts": counts
        }

        return Response(
            msg
        )


@api_view(['POST'])
def set_address(request, refer_code):
    address_id = request.POST["addressID"]
    user = request.user or None
    if user is None:
        return Response(
            {"msg": "You must authenticate!"}
        )
    order = get_object_or_404(Orders, customer=user, refer_code=refer_code)
    address = get_object_or_404(Address, owner=user, pk=address_id)
    order.address = address
    order.calc_discount()
    order.save()
    transaction = Transaction.objects.create(
        customer=user,
        status="w",
        refer_code=order.refer_code,
        order=order,
        amount=order.total_price

    )
    transaction.save()
    return Response("Success", status=200)

