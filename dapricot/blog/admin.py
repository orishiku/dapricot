from django.utils import timezone
from django.contrib import admin
from django.urls import path

from dapricot.blog.models import Post, Category, Tag, Comment, Commenter
from dapricot.blog import views

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author','status', 'last_edition_date']
    readonly_fields = ['slug','creation_date', 'last_edition_date', 'publication_date']
    ordering = ('-creation_date',)
    raw_id_fields = ('banner',)
    
    def save_model(self, request, obj, form, change):
        old_obj = Post.objects.filter(pk=obj.pk)
        
        if len(old_obj)>0:
            if obj.status =='p' and (old_obj.last().status !='p' or obj.publication_date==None):
                obj.publication_date = timezone.now()
        else: 
            if obj.status =='p':
                obj.publication_date = timezone.now()
                
        if obj.author is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:year>/<int:month>/<int:day>/<slug:slug>/<int:demo>', views.post, name='post_demo'),
        ]
        return my_urls + urls
    
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'status']
    readonly_fields = ['author', 'content']
    
@admin.register(Commenter)
class CommenterAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'email', 'status']