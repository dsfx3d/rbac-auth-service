from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
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
            'user_permissions'
        )
