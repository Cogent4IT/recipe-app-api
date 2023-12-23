""" Django admin customization."""

from django.contrib import admin
# creating "BaseUserAdmin" as alias of UserAdmin, in order to avoid conflict
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# for localization feature we import this package
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Defind the admin pages for users."""
    ordering = ["id"]
    list_display = ["email", "name"]
    # create tuple for fieldsets
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields":(
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            }
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets =(
        (None, {
            "classes": ("wide"),
            "fields": (
                "email",
                "password1",
                "password2",
                "name",
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),
    )


# registering the "UserAdmin" class above
admin.site.register(models.User, UserAdmin)