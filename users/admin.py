from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminModel(UserAdmin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'firstname', 'lastname', 'username', 'last_login', 'image')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'firstname', 'lastname', 'is_staff', 'last_login', 'image', 'pk')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def _allow_edit(self, obj=None):
        if not obj:
            return True
        return not (obj.is_staff or obj.is_superuser)

    def has_change_permission(self, request, obj=None):
        return self._allow_edit(obj)

    def has_delete_permission(self, request, obj=None):
        return self._allow_edit(obj)

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


admin.site.register(User, UserAdminModel)
