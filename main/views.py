from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework.routers import DefaultRouter

from .models import CustomUser, Answer
from .serializers import UserSerializer, AnswerSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserAPIView(ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | ReadOnly)]


class AnswerAPIView(ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | ReadOnly)]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Answer.objects.filter(client_id=user.id).order_by('-id')
        return Answer.objects.all().order_by('-id')


router = DefaultRouter()

router.register('users', UserAPIView)
router.register('answers', AnswerAPIView, basename='answer')
