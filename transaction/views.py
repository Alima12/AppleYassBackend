from django.shortcuts import render
from .serializers import OrderSerializer, TransactionSerializer, ManageOrdersSerializer, OrderItemSerializer, DiscountSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from .models import Orders, Transaction, Cart, OrderItem, Discount
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from utils.base_permissions import AdminRequired, IsAdminOrReadOnly
from product.models import Color


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, AdminRequired)

    def get_queryset(self):
        return Orders.objects.all().exclude(status="p")


class MyOrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Orders.objects.filter(customer=user).exclude(status="p")


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
        pass

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
            order.save()
            return Response("کد تخفیف با موفقیت اعمال شد")
        return Response("شما نمیتوانید از این کد تخفیف استفاده کنید")

    def get(self, request, code):
        user = request.user
        discount = get_object_or_404(Discount, code=code)
        order = Orders.objects.filter(customer=user, discount__code=discount.code).count()
        if not discount.is_active():
            msg = "مهلت استفاده از کد تخفیف مورد نظر به اتمام رسیده"
        elif order > 0 and not discount.reUseAble:
            msg = "شما قبلا از این کد تخفیف استاده کرده اید"
        else:
            data = DiscountSerializer(discount)
            msg = data.data

        return Response(
            msg
        )

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
