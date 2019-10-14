from django.db import models

class SecretsCollection(models.Model):
    name = models.SlugField(max_length=50, unique=True)
    is_applied = models.BooleanField(default=False, editable=False)
    
    def __str__(self):
        return self.name
    
    def counted_secrets(self):
        qs = self.get_secrets()
        
        return qs.count()
    
    def get_secrets(self):
        qs = Secret.objects.filter(collection=self)
        
        return qs
    
    def status(self):
        if self.is_applied:
            status_message = 'Active: Applied system-side'
            
        else:
            status_message = 'Inactive: Not applied system-side'
            
        return status_message

class Secret(models.Model):
    key_name = models.SlugField(max_length=50)
    value = models.CharField(max_length=100)
    collection = models.ForeignKey('SecretsCollection', on_delete=models.PROTECT)

    def __str__(self):
        return self.key_name

    class Meta:
        unique_together = (('key_name',  'collection'),)
