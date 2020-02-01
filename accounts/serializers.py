from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ('permissions',)


User = get_user_model()
class UserListSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        depth = 1
        fields = (
            'id',
            'email',
            'username',
            'is_superuser',
            'is_staff',
            'groups',
        )
