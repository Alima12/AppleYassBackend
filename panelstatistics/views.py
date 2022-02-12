from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.base_permissions import AdminRequired
from rest_framework.response import Response
from transaction.models import Orders, Transaction
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta


class DashboardApiView(APIView):
    permission_classes = (IsAuthenticated, AdminRequired)

    def get(self, request):
        user = request.user
        o_accepted = Orders.objects.filter(status="a").count()
        o_checked = Orders.objects.filter(status="c").count()
        o_delivered = Orders.objects.filter(status="d").count()
        o_returned = Orders.objects.filter(status="r").count()
        td = timezone.now()
        dif_10 = td - timedelta(days=10)
        dif_30 = td - timedelta(days=30)

        transactions_10 = Transaction.objects.filter(updated_at__gt=dif_10, status="s").aggregate(Sum("amount")) or 0
        transactions_30 = Transaction.objects.filter(updated_at__gt=dif_30, status="s").aggregate(Sum("amount")) or 0
        order_10 = Orders.objects.filter(updated_at__gt=dif_10).exclude(status="p").count()
        return Response({
            "msg": f"salam {user.first_name}",
            "orders": {
                "accepted": o_accepted,
                "checked": o_checked,
                "delivered": o_delivered,
                "returned": o_returned,
                "order_10": order_10
            },
            "transactions": {
                "last_10": transactions_10,
                "last_30": transactions_30,

            }
        }, status=200)

