from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
    GroupAdmin as BaseGroupAdmin
)
from django.contrib import admin
from .forms import UserChangeForm, UserCreationForm


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Groups', {'fields': ('groups',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


class UserInline(admin.TabularInline):
    '''Tabular Inline View for User'''

    model = Group.user_set.through
    min_num = 1
    max_num = 20
    extra = 1


admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    inlines = (UserInline,)
