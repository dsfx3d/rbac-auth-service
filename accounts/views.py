from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from rbac_auth.core.auth.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSlidingSerializer
)
from rbac_auth.core.permissions import DjangoModelPermissions
from rbac_auth.contrib.rest_framework.mixins import (
    DestroyModelMixin,
    SummarySerializerMixin,
)
from .serializers import (
    UserSummarySerializer,
    UserSerializer,
    GroupSummarySerializer,
    GroupSerializer,
    PermissionSerializer
)

from .mixins import RelatedEntityAPIView


User = get_user_model()

class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer

class TokenObtainSlidingView(TokenViewBase):
    serializer_class = TokenObtainSlidingSerializer

class UserListCreateAPIView(SummarySerializerMixin, ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = UserSerializer
    summary_serializer_class = UserSummarySerializer
    queryset = User.objects.all()

class UserRetrieveUpdateDestroyView(DestroyModelMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    soft_delete_field = 'is_active'

class UserGroupAPIView(RelatedEntityAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    related_model_class = Group
    related_field = 'groups'

class GroupListCreateView(SummarySerializerMixin, ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = GroupSerializer
    summary_serializer_class = GroupSummarySerializer
    queryset = Group.objects.all()

class GroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class GroupPermissionAPIView(RelatedEntityAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Group.objects.all()
    serializer_class = PermissionSerializer
    related_model_class = Permission
    related_field = 'permissions'
