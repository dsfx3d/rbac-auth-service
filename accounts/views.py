from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
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
    GroupPermissionSerializer,
    PermissionSerializer,
    PermissionsPayloadSerializer
)


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

class GroupListCreateView(SummarySerializerMixin, ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = GroupSerializer
    summary_serializer_class = GroupSummarySerializer
    queryset = Group.objects.all()

class GroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class GroupPermissionListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Group.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == 'GET':
            try:
                return queryset.get(pk=self.kwargs.get('pk')).permissions
            except Group.DoesNotExist:
                raise Http404
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PermissionSerializer
        else:
            return GroupPermissionSerializer

    def post(self, request, pk):
        perms_serializer = PermissionsPayloadSerializer(data=request.data)

        if perms_serializer.is_valid():
            group = self.get_object()
            permissions = Permission.objects.filter(
                id__in=perms_serializer.data.get('permissions')
            )

            for perm in permissions:
                group.permissions.add(perm)
                group.save()

            group_perms = PermissionSerializer(permissions, many=True)
            return Response(group_perms.data, status=status.HTTP_200_OK)

        else:
            return Response(perms_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupPermissionDestroyAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def delete(self):
        group = self.get_object(pk=self.kwargs.get('pk'))
        perm_id = self.kwargs.get('perm')
        group_perm = group.permissions.get(id=perm_id)
        group.permissions.remove(group_perm)
        return Response(status=status.HTTP_204_NO_CONTENT)
