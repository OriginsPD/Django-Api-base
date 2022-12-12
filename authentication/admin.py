""" Admin configuration for Account App """
from typing import Any, Sequence
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


from authentication.models import User


class UserAdminConfig(UserAdmin):
    """ User administration configuration """
    search_fields: Sequence[str] = (
        'email', 'username', 'first_name', 'last_name')
    ordering = ('-start_date',)
    list_filter: Sequence[str] = (
        'email', 'username', 'first_name', 'last_name')
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    fieldsets: tuple = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        # ('Personal', {'fields': ('email',)}),
    )

    add_fieldsets: Any = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name',
                       'password1', 'password2', 'is_staff', 'is_active',),
        }),
    )


# Register your models here.
admin.site.register(User, UserAdminConfig)
