from django.urls import path
from .views import (
    OrderListView,
    MyOrderListView,
    TransactionListView,
    ManageCart,
    OrderItemView,
    MyTransactionListView,
    DiscountListCreateView,
    DiscountDetailView,
    UpdateOrderItem,
    DiscountDetail,
    GetMyCheckout,
    ShoppingItems,
    set_address
)


urlpatterns = [
    path('', TransactionListView.as_view()),
    path('me/', MyTransactionListView.as_view()),

    path('orders/', OrderListView.as_view()),
    path('orders/shoppingview/<str:refer_code>/', ShoppingItems.as_view()),

    path('orders/me/', MyOrderListView.as_view()),
    path("orderitems/", OrderItemView.as_view()),
    path("order/cart/", ManageCart.as_view()),
    path("order/cart/update/<int:item>/", UpdateOrderItem.as_view()),
    path("order/cart/destroy/<int:item>/", UpdateOrderItem.as_view()),
    path("order/cart/checkout/", GetMyCheckout.as_view()),
    path("order/cart/checkout/set/<str:refer_code>/", set_address),


    path("discounts/", DiscountListCreateView.as_view()),
    path("discounts/<int:pk>/", DiscountDetailView.as_view()),
    path("discount/delete/", DiscountDetail.as_view()),
    path("discount/use/", DiscountDetail.as_view()),
    # path("discount/<str:code>/", DiscountDetail.as_view()),

]