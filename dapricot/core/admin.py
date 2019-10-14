from django.contrib import admin
from django.conf import settings
from dapricot.core.utils import SecretsCollectionObject
from dapricot.core.models import Secret, SecretsCollection

class SecretsHandlerModelAdmin(admin.ModelAdmin):
    using = 'secrets_db'
    
    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

class SecretsHandlerTabularInline(admin.TabularInline):
    using = 'secrets_db'
    
    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

def apply_system_side(modeladmin, request, queryset):
    for collection in queryset:
        c = SecretsCollectionObject(collection.name, settings.BASE_DIR)

        for secret in collection.get_secrets():
            c.add_or_change_secret_value(secret.key_name,
                                         secret.value)
        
        c.save_secrets()

        
    queryset.update(is_applied=True)
    
apply_system_side.short_description = "Apply secrets to be used system-side."

def remove_system_side(modeladmin, request, queryset):
    for collection in queryset:
        c = SecretsCollectionObject(collection.name, settings.BASE_DIR)

        for secret in collection.get_secrets():
            c.add_or_change_secret_value(secret.key_name,
                                         secret.value)
        
        c.save_secrets()

        
    queryset.update(is_applied=False)
    
remove_system_side.short_description = "Remove secrets to be used system-side."
    
class SecretInline(SecretsHandlerTabularInline):
    model = Secret
    
@admin.register(SecretsCollection)    
class CollectionAdmin(SecretsHandlerModelAdmin):
    list_display = ('name', 'counted_secrets', 'status')
    inlines = [SecretInline,]
    actions = [apply_system_side, remove_system_side]
    
    def get_queryset(self, request):
        qs = super(CollectionAdmin, self).get_queryset(request)
        djs = False
        dbs = False
        
        for collection in qs:
            if collection.name == 'DJANGO_SECRETS':
                djs = True
            elif collection.name == 'DATABASE_SECRETS':
                dbs = True
        
        if not djs:
            c = SecretsCollectionObject('DJANGO_SECRETS', settings.BASE_DIR)
            collection = SecretsCollection.objects.create(name='DJANGO_SECRETS')
            secrets = c.get_secrets()
            
            for secret in c.get_secrets():

                Secret.objects.create(key_name=secret,
                                      value=secrets[secret],
                                      collection=collection)

            collection.is_applied=True
            collection.save()
            
        if not dbs:
            c = SecretsCollectionObject('DATABASE_SECRETS', settings.BASE_DIR)
            collection = SecretsCollection.objects.create(name='DATABASE_SECRETS')
            secrets = c.get_secrets()
            
            for secret in c.get_secrets():

                Secret.objects.create(key_name=secret,
                                      value=secrets[secret],
                                      collection=collection)

            collection.is_applied=True
            collection.save()
        
        
        return super(CollectionAdmin, self).get_queryset(request)
            
            
            
            
            
            