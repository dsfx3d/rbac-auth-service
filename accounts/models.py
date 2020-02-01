from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from rbac_auth.core.auth.models import AbstractUser


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer (Letters, digits and @/./+/-/_)'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    AUTH_IDENTIFIERS = ('username', 'email',)
    REQUIRED_FIELDS = ('username',)
