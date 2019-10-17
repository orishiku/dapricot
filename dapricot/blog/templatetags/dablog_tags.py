from django import template
from django.core.paginator import Paginator

from dapricot.blog.models import Post

register = template.Library()

@register.simple_tag
def filter_posts_list(filter_name=None, value=None, page=1, page_limit=10):
    if filter_name=='category':
        posts = Post.objects.filter(status='p', category__slug=value)
    
    elif filter_name=='tag':
        posts = Post.objects.filter(status='p', tags__slug=value)
    
    else:
        posts = Post.objects.filter(status='p')

    return __posts_list(posts, page, page_limit)

@register.simple_tag
def date_posts_list(year, month=None, day=None, page=1, page_limit=10):
    posts = Post.objects.filter(status='p', publication_date__year=year)
    
    if month:
        posts = posts.filter(publication_date__month=month)

    if day:
        posts = posts.filter(publication_date__day=day)

    return __posts_list(posts, page, page_limit)

def __posts_list(posts, page, page_limit):
    posts = posts.order_by('-publication_date')
    paginator = Paginator(posts, page_limit)
    plist = paginator.get_page(page)
    
    return plist