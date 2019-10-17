from django.contrib import admin
from django.contrib.flatpages import admin as flatpage_admin

from dapricot.pages.models import Page

admin.site.unregister(flatpage_admin.FlatPage)

@admin.register(Page)
class PageAdmin(flatpage_admin.FlatPageAdmin):
    pass
