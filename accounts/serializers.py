from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class GroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ('permissions',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


User = get_user_model()
class BaseUserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)


class UserListCreateSerializer(BaseUserSerializer):
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
        return super(UserListCreateSerializer, self).create(validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )
