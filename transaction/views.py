from django.shortcuts import render
from .serializers import OrderSerializer, TransactionSerializer, ManageOrdersSerializer, OrderItemSerializer, DiscountSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from .models import Orders, Transaction, Cart, OrderItem, Discount
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from utils.base_permissions import AdminRequired, IsAdminOrReadOnly


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

    # def get(self, request):
    #     pass


class DiscountListCreateView(ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class DiscountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated, AdminRequired)




