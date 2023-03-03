from django.db.models import F
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.routers import DefaultRouter

from .models import Order
from .serializers import OrderSerializer


class OrderAPIView(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Order.objects.filter(client_id=user.id).annotate(client_number=F("client__number")).order_by("id")
        return Order.objects.all().annotate(client_number=F("client__number")).prefetch_related('orderfile_set').order_by("id")


router = DefaultRouter()
router.register("api/orders", OrderAPIView, basename="order")
