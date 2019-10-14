from django.contrib import admin
from django.conf import settings
from dapricot.integrations.models import Integration

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.user = request.user
        obj.save()