from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework.routers import DefaultRouter
from django_filters import rest_framework as filters

from .models import CustomUser, Answer, Order, Message
from .serializers import UserSerializer, AnswerSerializer, OrderSerializer, MessageSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserAPIView(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | ReadOnly)]


class AnswerAPIView(ReadOnlyModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | ReadOnly)]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Answer.objects.filter(order__client_id=user.id).order_by('-id')
        return Answer.objects.all().order_by('-id')


class MessageAPIView(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = {
        'creator__is_staff': ['exact'],
        'answer': ['exact'],
        'answer__order': ['exact'],
    }

    def perform_create(self, serializer):
        creator_id = self.request.user.id
        serializer.save(creator_id=creator_id)

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            queryset = Message.objects.filter(
                Q(creator_id=user.id) | Q(answer__order__client_id=user.id)
            ).order_by('-id')
        else:
            queryset = Message.objects.all().order_by('-id')
        return queryset.select_related('creator', 'answer__order', 'answer__order__client')


class OrderAPIView(ModelViewSet):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(client_id=self.request.user.id)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsAdminUser]
        elif self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [p() for p in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Order.objects.filter(client_id=user.id).order_by('-id')
        return Order.objects.all().order_by('-id')


router = DefaultRouter()
router.register('users', UserAPIView)
router.register('messages', MessageAPIView, basename='message')
router.register('orders', OrderAPIView, basename='order')
router.register('answers', AnswerAPIView, basename='answer')
