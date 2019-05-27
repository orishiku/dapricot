from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.blog')

default_app_config = 'dapricot.blog.apps.DapricotBlogConfig'