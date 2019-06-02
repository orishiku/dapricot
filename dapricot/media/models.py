from django.db import models
from django.utils.safestring import mark_safe

class Picture(models.Model):
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    
    picture = models.ImageField(upload_to="dapricot/pictures")
    
    def picture_preview(self):
        return mark_safe("<img src='/media/%s' height='100' />" % self.picture)
    
    picture_preview.short_description = 'Picture preview'
    
    def __str__(self):
        return self.name