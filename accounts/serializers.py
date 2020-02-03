from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = ('content_type',)
        depth = 1

class PermissionsPayloadSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.IntegerField())

class GroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ('permissions',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('permissions',)


User = get_user_model()
class BaseUserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)


class UserSummarySerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )

class UserSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        depth = 1
        fields = (
            'id',
            'email',
            'username',
            'is_superuser',
            'is_staff',
            'is_active',
            'groups',
            'password'
        )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
