from django.db import models
from django.contrib.auth import get_user_model

from dapricot.core.models import SecretsCollection

INTEGRATION_TYPE_OPTIONS = (
    ('twitter', 'Twitter'),)

def secrets_collection():
    collections = SecretsCollection.objects.all()
    return ((c.name, c.name) for c in collections)

class Integration(models.Model):
    type = models.CharField(max_length=10, choices=INTEGRATION_TYPE_OPTIONS)
    secrets = models.SlugField(max_length=50, choices=secrets_collection(), unique=True)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)
    
    def __str__(self):
        return "%s - %s" % (self.type, self.user)
    
    class Meta:
        unique_together = (('type',  'user'),)
    
    
    