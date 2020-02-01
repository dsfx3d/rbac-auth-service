from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer as BaseTokenObtainSerializer,
    PasswordField
)
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken

User = get_user_model()


class TokenObtainSerializer(BaseTokenObtainSerializer):
    username_field = 'username'
    identifier_field = 'identifier'
    identifier_choices = User.AUTH_IDENTIFIERS

    default_error_messages = {
        'no_active_account': _(
            'No active account found with the given credentials'
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()
        self.fields[self.identifier_field] = serializers.ChoiceField(
            choices=self.identifier_choices
        )

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
            self.identifier_field: attrs[self.identifier_field]
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` method for `TokenObtainSerializer`'
        )


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class TokenObtainSlidingSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return SlidingToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        token = self.get_token(self.user)

        data['token'] = str(token)

        return data
