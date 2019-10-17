from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from dapricot.auth.models import User, Group

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2'),
        }),
    )
    ordering = ('username','email',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username', 'email')
    readonly_fields = ('date_joined',)

admin.site.unregister(auth_admin.Group)
admin.site.register(Group,auth_admin.GroupAdmin)
