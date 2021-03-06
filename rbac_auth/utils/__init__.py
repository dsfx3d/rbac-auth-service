import re
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _


email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

validate_email = EmailValidator(email_re, _(u'Enter a valid e-mail address.'), 'invalid')


def is_sequence(arg):
    '''
    check if list or tuple
    '''
    return (
        not hasattr(arg, 'strip') and (
            hasattr(arg, '__getitem__') or hasattr(arg, '__iter__')
        )
    )
