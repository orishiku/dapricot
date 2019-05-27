from django.contrib import admin
from django.contrib.flatpages import admin as auth_admin
from django.utils.translation import gettext, gettext_lazy as _

from .models import Page

admin.site.unregister(auth_admin.FlatPage)

@admin.register(Page)
class PageAdmin(auth_admin.FlatPageAdmin):
    pass
