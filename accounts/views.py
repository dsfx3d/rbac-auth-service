from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from rbac_auth.core.auth.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSlidingSerializer
)
from rbac_auth.core.permissions import DjangoModelPermissions

from .serializers import UserSerializer


User = get_user_model()

class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer

class TokenObtainSlidingView(TokenViewBase):
    serializer_class = TokenObtainSlidingSerializer


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = User.objects.all()
