from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm
)


User = get_user_model()


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',)


class UserChangeForm(BaseUserChangeForm):

    class Meta:
        model = User
        fields = ('email',)
