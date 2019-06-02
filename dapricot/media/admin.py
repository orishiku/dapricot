from django.contrib import admin
from .models import Picture

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('picture_preview', 'name', 'description')