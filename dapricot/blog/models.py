from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.dispatch.dispatcher import receiver


ENTRY_STATUS_OPTIONS = (
    ('d','Draft'),
    ('p','Published'),
)
STATUS_COMMENT_OPTIONS = (
    ('a', 'Approved'),
    ('u', 'Under approvement'),)

STATUS_COMMENTER_OPTIONS = (
    ('v', 'Verified'),
    ('u', 'Under verification'),)

class Post(models.Model):
    title   = models.CharField(max_length=100)
    slug    = models.SlugField(max_length=100, blank=True)
    content = models.TextField()
    banner  = models.ForeignKey('damedia.Picture', 
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)

    tags     = models.ManyToManyField('Tag')
    status   = models.CharField(choices=ENTRY_STATUS_OPTIONS, max_length=1)
    category = models.ForeignKey('Category', 
                                 on_delete=models.SET_NULL,
                                 null=True) 
    
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    author          = models.ForeignKey(get_user_model(),
                                        on_delete=models.SET_NULL,
                                        null=True, editable=False)
    
    creation_date     = models.DateTimeField(auto_now_add=True, editable=False)
    last_edition_date = models.DateTimeField(auto_now=True, editable=False)
    publication_date  = models.DateTimeField(editable=False, null=True)
    
    @property
    def get_preview(self):
        preview_content = self.content.split('</p>')
        preview_content = strip_tags(preview_content[0])
        preview_content = preview_content[0:1000]
        
        return preview_content
    
    def get_absolute_url(self): 
        from django.urls import reverse
        
        if self.status == 'p':
            date=self.publication_date
            return reverse('dapricot_blog:post', kwargs={'day': date.day,
                                                         'month': date.month,
                                                         'year': date.year,
                                                         'slug':self.slug})

        else:
            date=self.last_edition_date
            return reverse('admin:post_demo', kwargs={'day': date.day,
                                                      'month': date.month,
                                                      'year': date.year,
                                                      'slug': self.slug,
                                                      'demo': 1})

    class Meta:
        verbose_name        = _('post')
        verbose_name_plural = _('posts')
        
        ordering = ('creation_date',)
        db_table = 'dapricot_blog_post'
        
        unique_together = ['title', 'slug']
        
    def __str__(self):
        return self.title
    
@receiver(post_save, sender=Post)
def post_slug(sender, instance, created, **kwargs):
    title = slugify(instance.title)[0:40]
    repeats = Post.objects.filter(slug=title).count()
    if repeats > 0:
        title += "_%s" % repeats
        
    instance.slug = title    
    if created:
        instance.save()

'''
'''
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    
    def save(self, *args, **kwargs):
        name = getattr(self, 'name')
        self.slug = slugify(name)
        
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'dapricot_blog_category'
        
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    
    def save(self, *args, **kwargs):
        name = getattr(self, 'name')
        self.slug = slugify(name)
        
        super(Tag, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        db_table = 'dapricot_blog_tag'
        
    def __str__(self):
        return self.name
    
class Commenter(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    
    status = models.CharField(
        choices=STATUS_COMMENTER_OPTIONS, 
        max_length=1, 
        default='u', 
        editable=False)
        
    class Meta:
        verbose_name = _('commenter')
        verbose_name_plural = _('commentators')
        db_table = 'dapricot_blog_commenter'
        
    def __str__(self):
        return self.nickname
    
    
class Comment(models.Model):
    content = models.TextField(max_length=500)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, editable=False)
    author = models.ForeignKey('Commenter', on_delete=models.CASCADE, editable=False)
    answer_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, editable=False)
    status = models.CharField(
        choices=STATUS_COMMENT_OPTIONS, 
        max_length=1, 
        default='u')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('creation_date',)
        db_table = 'dapricot_blog_comment'
    
    def __str__(self):
        return "{0} on {1}".format(self.author, self.post.permalink)
    
    